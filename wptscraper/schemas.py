from pydantic import BaseModel


class Player(BaseModel):
    first_name: str
    last_name: str


class RankingEntry(BaseModel):
    position: int
    player: Player
    points: int


class Ranking(BaseModel):
    ranking: list[RankingEntry]
