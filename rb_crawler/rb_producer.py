import logging

from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka.serialization import StringSerializer

from build.gen.bakdata.corporate.v1 import corporate_pb2
from build.gen.bakdata.corporate.v1.corporate_pb2 import Announcement, Corporate, Person
from rb_crawler.constant import SCHEMA_REGISTRY_URL, BOOTSTRAP_SERVER, RB_PERSONS, RB_CORPORATES, RB_ANNOUNCEMENTS

log = logging.getLogger(__name__)


class RbProducer:
    def __init__(self):
        schema_registry_conf = {"url": SCHEMA_REGISTRY_URL}
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)

        # Announcements
        protobuf_announcement_serializer = ProtobufSerializer(
            corporate_pb2.Announcement, schema_registry_client, {"use.deprecated.format": True}
        )
        producer_announcements_conf = {
            "bootstrap.servers": BOOTSTRAP_SERVER,
            "key.serializer": StringSerializer("utf_8"),
            "value.serializer": protobuf_announcement_serializer,
        }
        self.announcement_producer = SerializingProducer(producer_announcements_conf)

        # Persons
        protobuf_persons_serializer = ProtobufSerializer(
            corporate_pb2.Person, schema_registry_client, {"use.deprecated.format": True}
        )
        producer_persons_conf = {
            "bootstrap.servers": BOOTSTRAP_SERVER,
            "key.serializer": StringSerializer("utf_8"),
            "value.serializer": protobuf_persons_serializer,
        }
        self.persons_producer = SerializingProducer(producer_persons_conf)

        # Corporates
        protobuf_corporates_serializer = ProtobufSerializer(
            corporate_pb2.Corporate, schema_registry_client, {"use.deprecated.format": True}
        )
        producer_corporates_conf = {
            "bootstrap.servers": BOOTSTRAP_SERVER,
            "key.serializer": StringSerializer("utf_8"),
            "value.serializer": protobuf_corporates_serializer,
        }
        self.corporates_producer = SerializingProducer(producer_corporates_conf)

    def produce_announcement_to_topic(self, announcement: Announcement):
        self.announcement_producer.produce(
            topic=RB_ANNOUNCEMENTS, partition=-1, key=str(announcement.id), value=announcement, on_delivery=self.delivery_report
        )
        # It is a naive approach to flush after each produce this can be optimised
        self.announcement_producer.poll()

    def produce_corporate_to_topic(self, corporate: Corporate):
        self.corporates_producer.produce(
            topic=RB_CORPORATES, partition=-1, key=str(corporate.id), value=corporate, on_delivery=self.delivery_report
        )
        # It is a naive approach to flush after each produce this can be optimised
        self.corporates_producer.poll()

    def produce_person_to_topic(self, person: Person):
        self.persons_producer.produce(
            topic=RB_PERSONS, partition=-1, key=str(person.id), value=person, on_delivery=self.delivery_report
        )
        # It is a naive approach to flush after each produce this can be optimised
        self.persons_producer.poll()

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
