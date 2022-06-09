import logging

from util.constants import BOOTSTRAP_SERVER, SCHEMA_REGISTRY_URL

from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka.serialization import StringSerializer

log = logging.getLogger(__name__)

class KafkaProducer:
    def __init__(self, serialization_schema, topic):
        self.topic = topic
        schema_registry_conf = {"url": SCHEMA_REGISTRY_URL}
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)
        serializer = ProtobufSerializer(
            serialization_schema, schema_registry_client, {"use.deprecated.format": True}
        )
        producer_conf = {
            "bootstrap.servers": BOOTSTRAP_SERVER,
            "key.serializer": StringSerializer("utf_8"),
            "value.serializer": serializer,
        }
        self.producer = SerializingProducer(producer_conf)
    
    def produce(self, message, message_id):
        self.producer.produce(
            topic=self.topic, partition=-1, key=str(message_id), value=message, on_delivery=self.delivery_report
        )
        self.producer.poll()
    
    @staticmethod
    def delivery_report(err, msg):
        """
        Reports the failure or success of a message delivery.
        Args:
            err (KafkaError): The error that occurred on None on success.
            msg (Message): The message that was produced or failed.
        Note:
            In the delivery report callback the Message.key() and Message.value()
            will be the binary format as encoded by any configured Serializers and
            not the same object that was passed to produce().
            If you wish to pass the original object(s) for key and value to delivery
            report callback we recommend a bound callback or lambda where you pass
            the objects along.
        """
        if err is not None:
            log.error("Delivery failed for User record {}: {}".format(msg.key(), err))
            return
        log.info(
            "User record {} successfully produced to {} [{}] at offset {}".format(
                msg.key(), msg.topic(), msg.partition(), msg.offset()
            )
        )