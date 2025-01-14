import logging
from threading import Thread, Event

from util.constants import BOOTSTRAP_SERVER

from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from confluent_kafka.serialization import StringDeserializer

log = logging.getLogger(__name__)

class KafkaConsumer:
    def __init__(self, desirialization_schema, topic, consumer_id):
        self.stop = False
        self.topic = topic
        deserializer = ProtobufDeserializer(
            desirialization_schema, {"use.deprecated.format": True}
        )
        consumer_conf = {
            "bootstrap.servers": BOOTSTRAP_SERVER,
            "key.deserializer": StringDeserializer("utf_8"),
            "value.deserializer": deserializer,
            "auto.offset.reset": "earliest",
            "group.id": consumer_id
        }
        self.consumer = DeserializingConsumer(consumer_conf)
        self.consumer.subscribe([self.topic])
    
    def consume(self, callback):
        """ Starts consuming the given topic in an infinite loop

            Keyword arguments:
            callback -- a function that is called for each message. It should have one parameter of the message's type (see constructor)
        """
        self._kill_event = Event()
        self._thread = Thread(target=KafkaConsumer._consume_in_loop, args=(self.topic, self.consumer, callback, self._kill_event))
        self._thread.start()

    def _consume_in_loop(topic, consumer, callback, kill_event):
        log.info(f'Starting consumer thread for topic {topic}')
        while not kill_event.is_set():
            try:
                msg = consumer.poll(1.0)
                if msg is None:
                    log.debug("Recieved empty message. This might be due to a timeout")
                    continue
                value = msg.value()
                if value is None:
                    log.debug("Recieved empty value")
                    continue
                callback(value)
            except Exception as e:
                log.error(e)
        consumer.close()

    def terminate(self):
        """ Stops the consumer """
        log.info(f'Stopping consumer thread for topic {self.topic}')
        self._kill_event.set()