from abc import ABC
from abc import abstractmethod

from bs4.element import Tag
from httpx import Response
from pydantic import BaseModel

from wptscraper.schemas import Player
from wptscraper.schemas import Ranking
from wptscraper.schemas import RankingEntry


class Parser(ABC):
    def __init__(self, response: Response) -> None:
        self._response = response

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
        return Ranking([self._parse_entry(tag) for tag in entry_tags])
