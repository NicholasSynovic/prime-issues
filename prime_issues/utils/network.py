import requests


def checkURL(url: str) -> bool:
    response: int = requests.get(url=url).status_code

    match response:
        case 404:
            return False
        case _:
            return True


def postGraphQL(url: str, headers: dict[str, str], query: str) -> None:
    pass
