from build.gen.bakdata.corporate.v1.person_pb2 import Person
from util.kafka_consumer import KafkaConsumer


# The topic to consume
topic = "rb-persons"

# The consumer_id -> each message in 'topic' is delivered once per consumer_id
# Check 'Consumer Groups' in kowl
consumer_id = "MyExampleConsumer"

# The schema of the messages in 'topic'
schema = Person

# function is called for each person in topic that is consumed
# 'person' is of the same type as 'schema'
def print_person(person: Person):
    print(person.firstname + " " + person.lastname)

# Create an instance of KafkaConsumer
consumer = KafkaConsumer(schema, topic, consumer_id)

# register callback and start consuming
consumer.consume(print_person)