import logging
import os

import click

from trades_crawler import constants
from trades_crawler.trade_extractor import TradeExtractor

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
log = logging.getLogger(__name__)


@click.command()
@click.option("-i", "--issuer", "issuer", type=str, help="The issuer's first letter to start with (e.g. 'B')")
def run(issuer: str):
    log.warn("this is a warning")
    if issuer == "" or issuer is None:
        issuer = "A"
    elif not issuer in constants.ISSUERS:
        error = ValueError("The issuer parameter has to be an uppercase letter")
        log.error(error)
        exit(1)
    TradeExtractor(issuer).extract()

if __name__ == "__main__":
    run()
