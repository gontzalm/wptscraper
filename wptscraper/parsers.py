import re
from abc import ABC
from abc import abstractmethod

from bs4 import BeautifulSoup
from bs4.element import Tag
from pydantic import BaseModel

from wptscraper import schemas
from wptscraper.exceptions import ParsingError
from wptscraper.helpers import Gender


class Parser(ABC):
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup

    def _extract_data(
        self,
        selector: str,
        source: Tag | None = None,
        tag_attr: str | None = None,
    ) -> str:
        if source is None:
            source = self._soup

        if tag_attr is None:
            try:
                return source.select_one(selector).text  # type: ignore
            except AttributeError:
                raise ParsingError(type(self))

        try:
            return source.select_one(selector)[tag_attr]  # type: ignore
        except KeyError:
            raise ParsingError(type(self))

    @abstractmethod
    def parse(self) -> BaseModel:
        return NotImplementedError  # type: ignore


class RankingParser(Parser):
    _RANKING_SELECTOR = "li.c-player-card__item"
    _POSITION_SELECTOR = "div.c-player-card__position"
    _NAME_SELECTOR = "div.c-player-card__name"
    _IMAGE_SELECTOR = "div.c-player-card__img"
    _POINTS_SELECTOR = "div.c-player-card__score"
    _NAME_REGEX = re.compile(r"([A-Z][^A-Z]+)([A-Z][^A-Z]+)")

    def _parse_position(self, entry: tuple[int, Tag]) -> int:
        _, tag = entry
        position = self._extract_data(self._POSITION_SELECTOR, tag)
        return int(position)

    def _parse_player(self, entry: tuple[int, Tag]) -> schemas.Player:
        i, tag = entry
        full_name = self._extract_data(self._NAME_SELECTOR, tag)
        print(full_name)
        full_name = self._NAME_REGEX.match(full_name)
        gender = Gender.MALE if i < 10 else Gender.FEMALE
        image = (
            self._extract_data(self._IMAGE_SELECTOR, tag, "style")
            .split("(")[-1]
            .replace(")", "")
            .strip()
        )

        return schemas.Player(
            first_name=full_name.group(1),  # type: ignore
            last_name=full_name.group(2),  # type: ignore
            gender=gender,
            image=image,
        )

    def _parse_points(self, entry: tuple[int, Tag]) -> int:
        _, tag = entry
        points = self._extract_data(self._POINTS_SELECTOR, tag)
        return int(points)

    def _parse_entry(self, entry: tuple[int, Tag]) -> schemas.RankingEntry:
        return schemas.RankingEntry(
            position=self._parse_position(entry),
            player=self._parse_player(entry),
            points=self._parse_points(entry),
        )

    def parse(self) -> schemas.Ranking:
        ranking = self._soup.select(self._RANKING_SELECTOR)
        return schemas.Ranking(
            positions=[self._parse_entry(e) for e in enumerate(ranking)]
        )


class PlayerStatsParser(Parser):
    def parse(self) -> schemas.PlayerStats:
        player_stats = {}
        return schemas.PlayerStats(**player_stats)
