from httpx import AsyncClient
from httpx import Response
from pydantic import BaseModel

from config import Config
from wptscraper.parsers import Parser


class Scraper:
    BASE_URL = Config.BASE_URL

    def __init__(self, endpoint) -> None:
        self._client = AsyncClient(base_url=self.BASE_URL)
        self._endpoint = endpoint

    async def close(self):
        await self._client.aclose()

    async def _get(self) -> Response:
        target = "form_url_with_kwargs" + self._endpoint
        return await self._client.get(target)

    async def scrape(self, parser: Parser) -> BaseModel:
        parser.response = await self._get()
        return parser.parse()
