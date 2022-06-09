import logging
from time import sleep
import re
import requests
from parsel import Selector

from build.gen.bakdata.corporate.v1.corporate_pb2 import Announcement, Corporate, Status, Person
from rb_producer import RbProducer
from util.id_generator import get_person_id, get_corporate_id, get_announcement_id


log = logging.getLogger(__name__)


class RbExtractor:
    def __init__(self, start_rb_id: int, state: str):
        self.rb_id = start_rb_id
        self.state = state
        self.producer = RbProducer()

    def extract(self):
        while True:
            try:
                log.info(f"Sending Request for: {self.rb_id} and state: {self.state}")
                text = self.send_request()
                if "Falsche Parameter" in text:
                    log.info("The end has reached")
                    break
                selector = Selector(text=text)

                announcement = Announcement()
                announcement.rb_id = self.rb_id
                announcement.state = self.state
                announcement.reference_id = self.extract_company_reference_number(selector)
                event_type = selector.xpath("/html/body/font/table/tr[3]/td/text()").get()
                announcement.event_date = selector.xpath("/html/body/font/table/tr[4]/td/text()").get()
                announcement.id = get_announcement_id(self.rb_id, self.state)
                raw_text: str = selector.xpath("/html/body/font/table/tr[6]/td/text()").get()
                self.handle_events(announcement, event_type, raw_text)
                self.rb_id = self.rb_id + 1
                log.debug(announcement)

                person = Person()
                m = re.findall(" ([a-zA-Z\u0080-\uFFFF -]+), ([a-zA-Z\u0080-\uFFFF -]+), ([a-zA-Z\u0080-\uFFFF.\/ -]+), \*(\d{2}.\d{2}.\d{4}), ([a-zA-Z\u0080-\uFFFF,\/ -]+)", announcement.information)
                for i in range(0, len(m)):
                    person.lastname = m[i][1]
                    person.firstname = m[i][2]
                    person.placeofbirth = m[i][3]
                    person.birthday = m[i][4]
                    person.jobtitle = m[i][5]
                    person.id = get_person_id("rb", person.firstname, person.lastname)
                    self.producer.produce_person_to_topic(person=person)

                corporate = Corporate()
                corporate.name = announcement.information.split(",")[0]
                person.id = get_corporate_id("rb", corporate.name)
                self.producer.produce_corporate_to_topic(corporate=corporate)


            except Exception as ex:
                log.error(f"Skipping {self.rb_id} in state {self.state}")
                log.error(f"Cause: {ex}")
                self.rb_id = self.rb_id + 1
                continue
        exit(0)

    def send_request(self) -> str:
        url = f"https://www.handelsregisterbekanntmachungen.de/skripte/hrb.php?rb_id={self.rb_id}&land_abk={self.state}"
        # For graceful crawling! Remove this at your own risk!
        sleep(0.5)
        return requests.get(url=url).text

    @staticmethod
    def extract_company_reference_number(selector: Selector) -> str:
        return ((selector.xpath("/html/body/font/table/tr[1]/td/nobr/u/text()").get()).split(": ")[1]).strip()

    def handle_events(self, announcement, event_type, raw_text):
        if event_type == "Neueintragungen":
            self.handle_new_entries(announcement, raw_text)
        elif event_type == "Veränderungen":
            self.handle_changes(announcement, raw_text)
        elif event_type == "Löschungen":
            self.handle_deletes(announcement)

    def handle_new_entries(self, announcement: Announcement, raw_text: str) -> Announcement:
        log.debug(f"New company found: {announcement.id}")
        announcement.event_type = "create"
        announcement.information = raw_text
        announcement.status = Status.STATUS_ACTIVE
        self.producer.produce_announcement_to_topic(announcement=announcement)

    def handle_changes(self, announcement: Announcement, raw_text: str):
        log.debug(f"Changes are made to company: {announcement.id}")
        announcement.event_type = "update"
        announcement.status = Status.STATUS_ACTIVE
        announcement.information = raw_text
        self.producer.produce_announcement_to_topic(announcement=announcement)

    def handle_deletes(self, announcement: Announcement):
        log.debug(f"Company {announcement.id} is inactive")
        announcement.event_type = "delete"
        announcement.status = Status.STATUS_INACTIVE
        self.producer.produce_announcement_to_topic(announcement=announcement)
