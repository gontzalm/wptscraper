from datetime import date

from pydantic import BaseModel

from wptscraper.helpers import Gender


class Player(BaseModel):
    first_name: str
    second_name: str
    third_name: str | None
    gender: Gender
    image: str


class RankingEntry(BaseModel):
    position: int
    player: Player
    points: int


class Ranking(BaseModel):
    positions: list[RankingEntry]
    year: int = date.today().isocalendar().year
    week: int = date.today().isocalendar().week


class PlayerStats(BaseModel):
    # TODO
    player: Player
    more: list
