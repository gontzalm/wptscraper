class HttpClientConfig:
    BASE_URL = "https://www.worldpadeltour.com/en"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }


class EndpointsConfig:
    RANKING = "/players"
    PLAYER_STATS = "/players/<player>"
