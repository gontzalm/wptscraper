from bs4 import BeautifulSoup
from httpx import AsyncClient
from pydantic import BaseModel

from config import Config
from wptscraper.parsers import Parser


class Scraper:
    BASE_URL = Config.BASE_URL

    def __init__(self, endpoint: str, **path_params) -> None:
        self._client = AsyncClient(base_url=self.BASE_URL)
        self._endpoint = endpoint
        self._path_params = path_params

    @property
    def _target(self):
        for param, value in self._path_params.items():
            if param not in self._endpoint:
                raise ValueError(f"Param '{param}' not found in endpoint")
            self._endpoint.replace(param, value)
        return self._endpoint

    async def _get_soup(self) -> BeautifulSoup:
        r = await self._client.get(self._target)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")

    async def close(self):
        await self._client.aclose()

    async def scrape(self, parser: Parser) -> BaseModel:
        parser.soup = await self._get_soup()
        return parser.parse()
