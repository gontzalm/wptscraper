from __future__ import annotations

from abc import ABC

from bs4 import BeautifulSoup
from httpx import AsyncClient
from pydantic import BaseModel

from config import EndpointsConfig
from config import HttpClientConfig
from wptscraper import parsers


class Scraper(ABC):
    _BASE_URL = HttpClientConfig.BASE_URL
    _HEADERS = HttpClientConfig.HEADERS
    _PARSER: parsers.Parser = NotImplemented

    def __init__(self) -> None:
        self._client = AsyncClient(
            base_url=self._BASE_URL,
            headers=self._HEADERS,
        )
        self._endpoint: self._Endpoint = NotImplemented  # type: ignore

    async def __aenter__(self) -> Scraper:
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()

    async def _get_soup(self) -> BeautifulSoup:
        r = await self._client.get(self._endpoint.form())  # type: ignore
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")

    async def close(self):
        await self._client.aclose()

    async def scrape(self) -> BaseModel:
        soup = await self._get_soup()
        return self._PARSER(soup).parse()  # type: ignore

    class _Endpoint:
        def __init__(
            self,
            base_endpoint: str,
            path_params: dict[str, str] | None = None,
        ) -> None:
            self._base_endpoint = base_endpoint
            self._path_params = path_params

        def form(self) -> str:
            if self._path_params is None:
                return self._base_endpoint

            formed = self._base_endpoint
            for param, value in self._path_params.items():
                if param not in self._base_endpoint:
                    raise ValueError(f"Param '{param}' not found in endpoint")
                formed = formed.replace(f"<{param}>", value)
            return formed


class RankingScraper(Scraper):
    _PARSER = parsers.RankingParser  # type: ignore

    def __init__(self) -> None:
        super().__init__()
        self._endpoint = self._Endpoint(EndpointsConfig.RANKING)


class PlayerStatsScraper(Scraper):
    _PARSER = parsers.PlayerStatsParser  # type: ignore

    def __init__(self, name: str) -> None:
        super().__init__()
        self._endpoint = self._Endpoint(
            EndpointsConfig.PLAYER_STATS,
            path_params={"name": name},
        )  # type: ignore
