from httpx import AsyncClient

from config import Config
from wptscraper.parsers import PlayerParser
from wptscraper.parsers import RankingParser
from wptscraper.schemas import Player
from wptscraper.schemas import Ranking


class WptScraper:
    BASE_URL = Config.BASE_URL

    def __init__(self) -> None:
        self._session = AsyncClient(base_url=self.BASE_URL)

    async def get_ranking(self) -> Ranking:
        r = await self._session.get("/ranking")
        parser = RankingParser(r)
        return parser.parse()

    async def get_player(self, name) -> Player:
        r = await self._session.get(f"/players/{name}")
        parser = PlayerParser(r)
        return parser.parse()
