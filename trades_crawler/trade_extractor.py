import logging
from time import sleep
from numpy import NaN
import pandas as pd
from datetime import datetime

from trades_crawler import constants
from trades_crawler.trade_producer import TradeProducer
from build.gen.bakdata.trade.v1.trade_pb2 import Trade

log = logging.getLogger(__name__)

class TradeExtractor:
    def __init__(self, start_issuer: str):
        self.start_idx = constants.ISSUERS.index(start_issuer)
        self.producer = TradeProducer()

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
                    trade.bafin_id = row["BaFin-ID"]
                    trade.issuer = row["Emittent"]
                    trade.isin = row["ISIN"]
                    trade.reportable_person = row["Meldepflichtiger"]
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
                    trade.id = f"{trade.date_of_trade}_{trade.bafin_id}_{self.normalize(trade.reportable_person)}"
                    self.producer.produce_to_topic(trade)
                    log.debug(trade)                    
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