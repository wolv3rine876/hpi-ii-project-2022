import logging

from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka.serialization import StringSerializer

from build.gen.bakdata.trade.v1 import trade_pb2
from build.gen.bakdata.trade.v1.trade_pb2 import Trade, Person, Corporation, Company
from trades_crawler.constants import SCHEMA_REGISTRY_URL, BOOTSTRAP_SERVER, TRADE_TOPIC, PERSON_TOPIC, CORPORATIONS_TOPIC, COMPANIES_TOPIC

log = logging.getLogger(__name__)

class TradeProducer:
    def __init__(self):
        schema_registry_conf = {"url": SCHEMA_REGISTRY_URL}
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)

        protobuf_serializer = ProtobufSerializer(
            trade_pb2.Trade, schema_registry_client, {"use.deprecated.format": True}
        )

        producer_conf = {
            "bootstrap.servers": BOOTSTRAP_SERVER,
            "key.serializer": StringSerializer("utf_8"),
            "value.serializer": protobuf_serializer,
        }

        self.producer = SerializingProducer(producer_conf)

    def produce_trade(self, trade: Trade):
        self.producer.produce(
            topic=TRADE_TOPIC, partition=-1, key=str(trade.id), value=trade, on_delivery=self.delivery_report
        )
        # It is a naive approach to flush after each produce this can be optimised
        self.producer.poll()
    
    def produce_person(self, person: Person):
        self.producer.produce(
            topic=PERSON_TOPIC, partition=-1, key=str(person.id), value=person, on_delivery=self.delivery_report
        )
        # It is a naive approach to flush after each produce this can be optimised
        self.producer.poll()

    def produce_corporation(self, corporation: Corporation):
        self.producer.produce(
            topic=CORPORATIONS_TOPIC, partition=-1, key=str(corporation.id), value=corporation, on_delivery=self.delivery_report
        )
        # It is a naive approach to flush after each produce this can be optimised
        self.producer.poll()

    def produce_company(self, company: Company):
        self.producer.produce(
            topic=COMPANIES_TOPIC, partition=-1, key=str(company.id), value=company, on_delivery=self.delivery_report
        )
        # It is a naive approach to flush after each produce this can be optimised
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
