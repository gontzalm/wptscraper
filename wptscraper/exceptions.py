class WptScraperError(Exception):
    pass


class ParsingError(WptScraperError):
    def __init__(self, parser) -> None:
        super().__init__(
            f"Parser '{parser}' could not parse the soup. Please check its parsing logic"
        )
