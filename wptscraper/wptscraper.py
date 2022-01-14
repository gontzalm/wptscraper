import logging

from pydantic import BaseModel

from wptscraper import schemas
from wptscraper import scrapers
from wptscraper.helpers import prettify

logger = logging.getLogger(__name__)


class WptScraper:
    async def get_ranking(self) -> schemas.Ranking:
        logger.info("Getting WPT ranking")
        ranking = await self.ResourceGetter(scrapers.RankingScraper()).get()
        logger.info("Successfuly got WPT ranking")
        return ranking  # type: ignore

    async def get_player_stats(self, name: str) -> schemas.Player:
        logger.info("Getting %s's current stats", prettify(name))
        player = await self.ResourceGetter(scrapers.PlayerStatsScraper(name)).get()
        logger.info("Successfuly got %s's current stats", prettify(name))
        return player  # type: ignore

    class ResourceGetter:
        def __init__(self, scraper: scrapers.Scraper) -> None:
            self._scraper = scraper  # type: ignore

        async def get(self) -> BaseModel:
            async with self._scraper as s:
                return await s.scrape()
