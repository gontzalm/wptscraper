from abc import ABC
from abc import abstractmethod

from bs4 import BeautifulSoup
from bs4.element import Tag
from pydantic import BaseModel

from wptscraper.schemas import Player
from wptscraper.schemas import Ranking
from wptscraper.schemas import RankingEntry


class Parser(ABC):
    def __init__(self):
        self._soup = None

    @property
    def soup(self) -> BeautifulSoup:
        if self._soup is None:
            raise AttributeError(
                f"Must set 'soup' instance variable in '{type(self)}' object"
            )
        return self._soup

    @soup.setter
    def soup(self, val: BeautifulSoup) -> None:
        self._soup = val

    @abstractmethod
    def parse(self) -> BaseModel:
        return NotImplementedError  # type: ignore


class PlayerParser(Parser):
    def parse(self) -> Player:
        player = {}
        return Player(**player)


class RankingParser(Parser):
    def _parse_entry(self, tag: Tag) -> RankingEntry:
        ranking_entry = {}
        return RankingEntry(**ranking_entry)

    def parse(self) -> Ranking:
        entry_tags = []
        return Ranking(ranking=[self._parse_entry(tag) for tag in entry_tags])
