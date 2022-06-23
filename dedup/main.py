from util.kafka_consumer import KafkaConsumer
from util.kafka_producer import KafkaProducer
from build.gen.bakdata.corporate.v1.person_pb2 import Person
from bisect import bisect_left, insort_left
from util.id_generator import normalize
from pyjarowinkler import distance
import click
import logging

log = logging.getLogger(__name__)

names = []

@click.command()
@click.option("--topic", help="Enter the topic you want to run the deduplication on.")
def run(topic):
    print("Finding duplicates in {} ...".format(topic))
    consumer = KafkaConsumer(Person, topic, "Dedup Consumer")
    consumer.consume(process_message)

def process_message(person: Person):
    name = normalize(person.firstname + " " + person.lastname)
    if len(names) == 0:
        insort_left(names, name)
    else:
        found_duplicate = False
        insertion_point = bisect_left(names, name)
        for i in range(max(0, insertion_point - 2), min(len(names), insertion_point + 2)):
            if distance.get_jaro_distance(name, names[i], winkler=False) > 0.95:
                found_duplicate = True
                print("Found duplicate: {} - {} -- JW: {}".format(names[i], name, distance.get_jaro_distance(name, names[i], winkler=False)))                
        if found_duplicate == False:
            insort_left(names, name)
            # to be done: produce to dedup topic

if __name__ == "__main__":
    run()