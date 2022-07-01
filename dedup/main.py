import logging
import os
import click
from dedup import Dedup

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
log = logging.getLogger(__name__)

@click.command()
@click.option("--topic_type", help="Enter the topic you want to run the deduplication on.")
def run(topic_type):
    Dedup(topic_type).dedup()

if __name__ == "__main__":
    run()