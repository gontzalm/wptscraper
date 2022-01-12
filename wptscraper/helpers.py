def prettify(string: str) -> str:
    return " ".join([w.capitalize() for w in string.split("-")])
