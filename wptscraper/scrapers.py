from abc import ABC
from abc import abstractmethod

from bs4 import BeautifulSoup
from httpx import AsyncClient
from pydantic import BaseModel

from config import EndpointsConfig
from config import HttpClientConfig
from wptscraper import parsers
from wptscraper.helpers import Endpoint


class Scraper(ABC):
    _BASE_URL = HttpClientConfig.BASE_URL
    _HEADERS = HttpClientConfig.HEADERS

    def __init__(self) -> None:
        self._client = AsyncClient(
            base_url=self._BASE_URL,
            headers=self._HEADERS,
        )

    @property
    @classmethod
    @abstractmethod
    def _ENDPOINT(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def _PARSER(cls):
        return NotImplementedError

    async def _get_soup(self) -> BeautifulSoup:
        r = await self._client.get(type(self)._ENDPOINT.form())  # type: ignore
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")

    async def close(self):
        await self._client.aclose()

    async def scrape(self) -> BaseModel:
        soup = await self._get_soup()
        return type(self)._PARSER(soup).parse()  # type: ignore


class PlayerStatsScraper(Scraper):
    _ENDPOINT = Endpoint(EndpointsConfig.PLAYER_STATS)  # type: ignore
    _PARSER = parsers.PlayerStatsParser  # type: ignore


class RankingScraper(Scraper):
    _ENDPOINT = Endpoint(EndpointsConfig.RANKING)  # type: ignore
    _PARSER = parsers.RankingParser  # type: ignore
