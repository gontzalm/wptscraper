import logging

from databases import Database

from wptscraper import parsers
from wptscraper import schemas
from wptscraper.helpers import prettify
from wptscraper.scraper import Scraper

# from config import Config

logger = logging.getLogger(__name__)


class WptScraper:
    def __init__(self) -> None:
        pass

    async def get_player(self, name: str) -> schemas.Player:
        logger.info("Getting player %s", prettify(name))
        scraper = Scraper("/players/<player>", player=name)
        player = await scraper.scrape(parsers.PlayerParser())
        logger.info("Successfuly got player %s", prettify(name))
        return player  # type: ignore

    async def get_ranking(self) -> schemas.Ranking:
        logger.info("Getting WPT ranking")
        scraper = Scraper("/players")
        ranking = await scraper.scrape(parsers.RankingParser())
        logger.info("Successfuly got WPT ranking")
        return ranking  # type: ignore

    async def update_database(self, db: Database) -> None:
        return NotImplementedError  # type: ignore
