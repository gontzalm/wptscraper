from enum import Enum


def prettify(string: str) -> str:
    return " ".join([w.capitalize() for w in string.split("-")])


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
