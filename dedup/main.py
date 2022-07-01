from util.kafka_consumer import KafkaConsumer
from util.kafka_producer import KafkaProducer
from build.gen.bakdata.corporate.v1.person_pb2 import Person as RbPerson
from build.gen.bakdata.trade.v1.person_pb2 import Person as TradesPerson
from bisect import bisect_left, insort_left
from util.id_generator import normalize
from pyjarowinkler import distance
import click
import logging
import threading

log = logging.getLogger(__name__)
sem = threading.Semaphore()
names = []

@click.command()
@click.option("--topic_type", help="Enter the topic you want to run the deduplication on.")
def run(topic_type):
    if topic_type == "persons":
        print("Finding duplicates for trades-persons ...")
        trades_persons_consumer = KafkaConsumer(TradesPerson, "trade-persons", "dedup_trades-person2")
        trades_persons_producer = KafkaProducer
        trades_persons_consumer.consume(process_trades_person)
        print("Finding duplicates for rb-persons ...")
        rb_persons_consumer = KafkaConsumer(RbPerson, "rb-persons", "dedup_rb-person2")
        rb_persons_consumer.consume(process_rb_person)

def process_rb_person(rb_person: RbPerson):
    name = normalize(rb_person.firstname + " " + rb_person.lastname)
    sem.acquire()
    if len(names) == 0:
        insort_left(names, name)
    else:
        found_duplicate = False
        jaro_dist = 0
        insertion_point = bisect_left(names, name)
        for i in range(max(0, insertion_point - 2), min(len(names), insertion_point + 2)):
            jaro_dist = distance.get_jaro_distance(name, names[i], winkler=False)
            if jaro_dist > 0.95:
                found_duplicate = True
                # produce to topic with dedup_id = hash(names[i])
                if jaro_dist == 1.0:
                    print("Found exact duplicate for person from trades-persons: {} - {} -> JW: {}".format(names[i], name, jaro_dist))
                else:
                    print("[!] Found fuzzy duplicate for person from trades-persons: {} - {} -> JW: {}".format(names[i], name, jaro_dist))
                break               
        if found_duplicate == False:
            insort_left(names, name)
            # produce to topic with dedup_id = hash(name)
    sem.release()

def process_trades_person(trades_person: TradesPerson):
    name = normalize(trades_person.firstname + " " + trades_person.name)
    sem.acquire()
    if len(names) == 0:
        insort_left(names, name)
    else:
        found_duplicate = False
        jaro_dist = 0
        insertion_point = bisect_left(names, name)
        for i in range(max(0, insertion_point - 2), min(len(names), insertion_point + 2)):
            jaro_dist = distance.get_jaro_distance(name, names[i], winkler=False)
            if jaro_dist > 0.95:
                found_duplicate = True
                # produce to topic with dedup_id = hash(names[i])
                if jaro_dist == 1.0:
                    print("Found exact duplicate for person from trades-persons: {} - {} -> JW: {}".format(names[i], name, jaro_dist))
                else:
                    print("[!] Found fuzzy duplicate for person from trades-persons: {} - {} -> JW: {}".format(names[i], name, jaro_dist))
                break               
        if found_duplicate == False:
            insort_left(names, name)
            # produce to topic with dedup_id = hash(name)
    sem.release()

if __name__ == "__main__":
    run()