import logging
from time import sleep
from numpy import NaN
import pandas as pd
from datetime import datetime

from trades_crawler import constants
#from trades_crawler.trade_producer import TradeProducer
from constants import TRADE_TOPIC, PERSON_TOPIC, CORPORATIONS_TOPIC, COMPANIES_TOPIC
from build.gen.bakdata.trade.v1.trade_pb2 import Trade
from build.gen.bakdata.trade.v1.person_pb2 import Person
from build.gen.bakdata.trade.v1.corporation_pb2 import Corporation
from build.gen.bakdata.trade.v1.company_pb2 import Company
from util import id_generator
from util.kafka_producer import KafkaProducer

log = logging.getLogger(__name__)

class TradeExtractor:
    def __init__(self, start_issuer: str):
        self.start_idx = constants.ISSUERS.index(start_issuer)
        self.trade_producer = KafkaProducer(Trade, TRADE_TOPIC)
        self.person_producer = KafkaProducer(Person, PERSON_TOPIC)
        self.corporation_producer = KafkaProducer(Corporation, CORPORATIONS_TOPIC)
        self.company_producer = KafkaProducer(Company, COMPANIES_TOPIC)

    def extract(self):
        for letter in constants.ISSUERS[self.start_idx:]:
            try:
                log.info(f"Sending Request for issuer: {letter}")
                df = pd.read_csv(f"https://portal.mvp.bafin.de/database/DealingsInfo/sucheForm.do?meldepflichtigerName=&zeitraum=0&d-4000784-e=1&emittentButton=Suche+Emittent&emittentName={letter}&zeitraumVon=&emittentIsin=&6578706f7274=1&zeitraumBis=", sep=";")
                log.debug(f"Recieved {len(df.index)} rows")
                # replace empty values
                df = df.fillna("")
                for _, row in df.iterrows():
                    trade = Trade()
                    # extract
                    person = self.get_person(row["Meldepflichtiger"])
                    if person is not None:
                        trade.personid = person.id
                    # Meldepflichtiger can be a company
                    company = self.get_company(row["Meldepflichtiger"])
                    if company is not None:
                        trade.companyid = company.id
                    corporation = Corporation()
                    corporation.name = row["Emittent"]
                    corporation.id = id_generator.get_corporate_id(corporation.name)
                    corporation.bafin_id = row["BaFin-ID"]
                    corporation.isin = row["ISIN"]
                    trade.issuerid = corporation.id
                    trade.position = row["Position / Status"]
                    trade.asset_type = row["Art des Instruments"]
                    trade.trade_type = row["Art des Geschäfts"]
                    ap, apc = self.split_currency(row["Durchschnittspreis"])
                    trade.avg_price = ap
                    trade.avg_price_currency = apc
                    av, avc = self.split_currency(row["Aggregiertes Volumen"])
                    trade.aggregate_volume = av
                    trade.aggregate_volume_currency = avc
                    trade.date_of_notification = self.date_to_ISO(row["Mitteilungsdatum"])
                    trade.date_of_trade = self.date_to_ISO(row["Datum des Geschäfts"])
                    trade.place_of_trade = row["Ort des Geschäfts"]
                    trade.date_of_activation = self.datetime_to_ISO(row["Datum der Aktivierung"])
                    trade.id = id_generator.get_trade_id(trade.date_of_trade, trade.issuerid, trade.personid)
                    # produce
                    self.trade_producer.produce(trade, trade.id)
                    self.corporation_producer.produce(corporation, corporation.id)
                    if person is not None:
                        self.person_producer.produce(person, person.id)
                    if company is not None:
                        self.company_producer.produce(company, company.id)                    
            except Exception as ex:
                log.error(f"Skipping issuers starting with letter {letter}")
                log.error(f"Cause: {ex.with_traceback()}")
                break
            sleep(0.5)

    def date_to_ISO(self, date_str:str):
        return datetime.strptime(date_str, "%d.%m.%Y").date().isoformat()

    def datetime_to_ISO(self, datetime_str:str):
        return datetime.strptime(datetime_str, "%d.%m.%Y %H:%M:%S").isoformat()

    """ Splits a string that has a whitespace and a currency  at the end into a double and a str
        E.g. 10.000 EUR -> 10000, "EUR"
    """
    def split_currency(self, value: str):
        if value is None or value == "":
            return 0.0, ""
        idx = value.find(" ")
        return float(value[:idx].replace(".","").replace(",",".")), value[idx+1:]

    """ Removes special characters from a string"""
    def normalize(self, s:str):
        return ''.join(e for e in s if e.isalnum())

    def get_person(self, name:str):
        # Not a name -> probably a company
        if not ", " in name:
            return None
        person = Person()
        split = name.split(", ")
        person.name = split[0]
        split = split[1].split(" ")
        person.title =  " ".join([s for s in split if '.' in s])
        person.firstname = " ".join([s for s in split if not "." in s])
        person.id = id_generator.get_person_id(person.firstname, person.name)
        return person
    
    def get_company(self, name:str):
        # Not a corporate -> probably a company
        if ", " in name:
            return None
        company = Company()
        company.id = id_generator.get_corporate_id(name)
        company.name = name
        return company