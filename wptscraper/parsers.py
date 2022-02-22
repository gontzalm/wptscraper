import re
from abc import ABC
from abc import abstractmethod

from bs4 import BeautifulSoup
from bs4.element import Tag
from pydantic import BaseModel

from wptscraper import schemas
from wptscraper.helpers import Gender


class Parser(ABC):
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup

    def _extract_tags(self, selector: str) -> list[Tag]:
        return self._soup.select(selector)

    def _extract_data(
        self,
        tag: Tag,
        selector: str,
        tag_attr: str | None = None,
    ) -> str:
        target_tag = tag.select_one(selector)
        if tag_attr is None:
            return target_tag.text  # type: ignore
        return target_tag[tag_attr]  # type: ignore

    @abstractmethod
    def parse(self) -> BaseModel:
        return NotImplementedError  # type: ignore


class RankingParser(Parser):
    _RANKING_SELECTOR = "li.c-player-card__item"
    _POSITION_SELECTOR = "div.c-player-card__position"
    _NAME_SELECTOR = "div.c-player-card__name"
    _IMAGE_SELECTOR = "div.c-player-card__img"
    _POINTS_SELECTOR = "div.c-player-card__score"
    _NAME_REGEX = re.compile(r"([A-Z][^A-Z]+)([A-Z][^A-Z]+)([A-Z][^A-Z]+)?")

    def _parse_position(self, entry: tuple[int, Tag]) -> int:
        _, tag = entry
        position = self._extract_data(tag, self._POSITION_SELECTOR)
        return int(position)

    def _parse_player(self, entry: tuple[int, Tag]) -> schemas.Player:
        i, tag = entry
        full_name = self._extract_data(tag, self._NAME_SELECTOR)
        full_name = self._NAME_REGEX.match(full_name)
        first_name, second_name = full_name.group(1), full_name.group(2)  # type: ignore
        third_name = full_name.group(3)  # type: ignore
        gender = Gender.MALE if i < 10 else Gender.FEMALE
        image = (
            self._extract_data(tag, self._IMAGE_SELECTOR, "style")
            .split("(")[-1]
            .replace(")", "")
            .strip()
        )
        return schemas.Player(
            first_name=first_name,
            second_name=second_name,
            third_name=third_name,
            gender=gender,
            image=image,
        )

    def _parse_points(self, entry: tuple[int, Tag]) -> int:
        _, tag = entry
        points = self._extract_data(tag, self._POINTS_SELECTOR)
        return int(points)

    def _parse_entry(self, entry: tuple[int, Tag]) -> schemas.RankingEntry:
        return schemas.RankingEntry(
            position=self._parse_position(entry),
            player=self._parse_player(entry),
            points=self._parse_points(entry),
        )

    def parse(self) -> schemas.Ranking:
        ranking = self._extract_tags(self._RANKING_SELECTOR)
        return schemas.Ranking(
            positions=[self._parse_entry(e) for e in enumerate(ranking)]
        )


class PlayerStatsParser(Parser):
    def parse(self) -> schemas.PlayerStats:
        player_stats = {}
        return schemas.PlayerStats(**player_stats)
