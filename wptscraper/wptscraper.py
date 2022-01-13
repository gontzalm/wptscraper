import logging

from wptscraper import schemas
from wptscraper import scrapers
from wptscraper.helpers import prettify

logger = logging.getLogger(__name__)


class WptScraper:
    async def get_ranking(self) -> schemas.Ranking:
        logger.info("Getting WPT ranking")
        scraper = scrapers.RankingScraper()
        try:
            ranking = await scraper.scrape()
            logger.info("Successfuly got WPT ranking")
        finally:
            await scraper.close()
        return ranking  # type: ignore

    async def get_player_stats(self, name: str) -> schemas.Player:
        logger.info("Getting player %s", prettify(name))
        scraper = scrapers.PlayerStatsScraper()
        try:
            player = await scraper.scrape()
            logger.info("Successfuly got player %s", prettify(name))
        finally:
            await scraper.close()
        return player  # type: ignore
