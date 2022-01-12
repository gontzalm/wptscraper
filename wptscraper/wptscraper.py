import logging

from databases import Database

from wptscraper import schemas
from wptscraper.helpers import prettify
from wptscraper.scraper import Scraper

# from config import Config

logger = logging.getLogger(__name__)


class WptScraper:
    def __init__(self) -> None:
        pass

    async def get_player(self, name) -> schemas.Player:
        logger.info("Getting player %s", prettify(name))
        scraper = Scraper("/players/<player>")
        player = await scraper.scrape()
        logger.info("Successfuly got player %s", prettify(name))
        return player

    async def get_ranking(self) -> schemas.Ranking:
        logger.info("Getting WPT ranking")
        scraper = Scraper("/players")
        ranking = await scraper.scrape()
        logger.info("Successfuly got WPT ranking")
        return ranking

    async def update_database(self, db: Database) -> None:
        return NotImplementedError  # type: ignore
