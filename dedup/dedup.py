from util.kafka_consumer import KafkaConsumer
from util.kafka_producer import KafkaProducer
from build.gen.bakdata.corporate.v1.person_pb2 import Person as RbPerson
from build.gen.bakdata.trade.v1.person_pb2 import Person as TradesPerson
from build.gen.bakdata.dedup.v1.person_pb2 import Person as DedupPerson
from bisect import bisect_left, insort_left
from util.id_generator import normalize, hash
from pyjarowinkler import distance
from constants import TRADES_PERSONS_TOPIC, RB_PERSONS_TOPIC, DEDUP_PERSONS_TOPIC
import click
import logging
import threading
import sys

log = logging.getLogger(__name__)
sem = threading.Semaphore()

class Dedup:
    def __init__(self, topic_type):
        if topic_type == "persons":
            self.names = []
            self.trades_persons_consumer = KafkaConsumer(TradesPerson, TRADES_PERSONS_TOPIC, "dedup_trades-person6")
            self.trades_person_producer = KafkaProducer(DedupPerson, DEDUP_PERSONS_TOPIC)
            self.rb_persons_consumer = KafkaConsumer(RbPerson, RB_PERSONS_TOPIC, "dedup_rb-person6")
            self.rb_person_producer = KafkaProducer(DedupPerson, DEDUP_PERSONS_TOPIC)
        else:
            sys.exit("You must define a valid topic for deduplication.")

    def dedup(self):
            self.trades_persons_consumer.consume(self.process_trades_person)
            print("Finding duplicates for trades-persons ...")
            self.rb_persons_consumer.consume(self.process_rb_person)
            print("Finding duplicates for rb-persons ...")

    def process_rb_person(self, rb_person: RbPerson):
        name = normalize(rb_person.firstname + " " + rb_person.lastname)
        sem.acquire()
        if len(self.names) == 0:
            insort_left(self.names, name)
        else:
            found_duplicate = False
            jaro_dist = 0
            dedup_person = DedupPerson()
            dedup_person.id = rb_person.id
            insertion_point = bisect_left(self.names, name)
            # compare against 10 most similar names in sorted list
            for i in range(max(0, insertion_point - 2), min(len(self.names), insertion_point + 2)):
                jaro_dist = distance.get_jaro_distance(name, self.names[i], winkler=False)
                if jaro_dist > 0.96:
                    found_duplicate = True
                    # produce to dedup topic with dedup id = hash(nameof(duplicate partner))
                    dedup_person.dedup_id = hash(self.names[i])
                    self.rb_person_producer.produce(dedup_person, dedup_person.id)
                    if jaro_dist == 1.0:
                        print("Found exact duplicate for person from trades-persons: {} - {} -> JW: {}".format(self.names[i], name, jaro_dist))
                    else:
                        print("[!] Found fuzzy duplicate for person from trades-persons: {} - {} -> JW: {}".format(self.names[i], name, jaro_dist))
                    break 
            #duplicate not found -> produce to topic with dedup_id = hash(own name)             
            if found_duplicate == False:
                insort_left(self.names, name)
                dedup_person.dedup_id = hash(name)
                self.rb_person_producer.produce(dedup_person, dedup_person.id)
        sem.release()

    def process_trades_person(self, trades_person: TradesPerson):
        name = normalize(trades_person.firstname + " " + trades_person.name)
        sem.acquire()
        if len(self.names) == 0:
            insort_left(self.names, name)
        else:
            found_duplicate = False
            jaro_dist = 0
            dedup_person = DedupPerson()
            dedup_person.id = trades_person.id
            insertion_point = bisect_left(self.names, name)            
            # compare against 10 most similar names in sorted list
            for i in range(max(0, insertion_point - 2), min(len(self.names), insertion_point + 2)):
                jaro_dist = distance.get_jaro_distance(name, self.names[i], winkler=False)
                if jaro_dist > 0.96:
                    found_duplicate = True
                    # produce to dedup topic with dedup id = hash(nameof(duplicate partner))
                    dedup_person.dedup_id = hash(self.names[i])
                    self.trades_person_producer.produce(dedup_person, dedup_person.id)
                    if jaro_dist == 1.0:
                        print("Found exact duplicate for person from trades-persons: {} - {} -> JW: {}".format(self.names[i], name, jaro_dist))
                    else:
                        print("[!] Found fuzzy duplicate for person from trades-persons: {} - {} -> JW: {}".format(self.names[i], name, jaro_dist))
                    break    
            #duplicate not found -> produce to topic with dedup_id = hash(own name)                        
            if found_duplicate == False:
                insort_left(self.names, name)
                dedup_person.dedup_id = hash(name)
                self.trades_person_producer.produce(dedup_person, dedup_person.id)
        sem.release()