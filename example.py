from build.gen.bakdata.corporate.v1.person_pb2 import Person as RB_Person
from build.gen.bakdata.trade.v1.person_pb2 import Person as Trade_Person
from util.kafka_consumer import KafkaConsumer


# The topic to consume
topic = "rb-persons"
topic2 = "trade-persons"

# The consumer_id -> each message in 'topic' is delivered once per consumer_id
# Check 'Consumer Groups' in kowl
consumer_id = "MyExampleDoubleConsumer2"

# The schema of the messages in 'topic'
schema = RB_Person
schema2 = Trade_Person

# function is called for each person in topic that is consumed
# 'person' is of the same type as 'schema'
def print_rb_person(person: RB_Person):
    print("RB Person: " + person.firstname + " " + person.lastname)

def print_trade_person(person: Trade_Person):
    print("Trade Person: " + person.firstname + " " + person.name)

# Create an instance of KafkaConsumer
rb_consumer = KafkaConsumer(schema, topic, consumer_id)
trade_consumer = KafkaConsumer(schema2, topic2, consumer_id)

# register callback and start consuming
rb_consumer.consume(print_rb_person)
trade_consumer.consume(print_trade_person)