from enum import Enum


def prettify(string: str) -> str:
    return " ".join([w.capitalize() for w in string.split("-")])


class Endpoint:
    def __init__(
        self, endpoint: str, path_params: dict[str, str] | None = None
    ) -> None:
        self._endpoint = endpoint
        self._path_params = path_params

    def form(self) -> str:
        if self._path_params is None:
            return self._endpoint

        for param, value in self._path_params.items():
            if param not in self._endpoint:
                raise ValueError(f"Param '{param}' not found in endpoint")
            self._endpoint.replace(f"<{param}>", value)
        return self._endpoint


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
