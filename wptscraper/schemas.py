from datetime import date

from pydantic import BaseModel

from wptscraper.helpers import Gender


class Player(BaseModel):
    first_name: str
    last_name: str
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
