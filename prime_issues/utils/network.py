from json import loads

from requests import Response, get, post


def checkURL(url: str) -> bool:
    responseCode: int = get(url=url).status_code

    match responseCode:
        case 404:
            return False
        case _:
            return True


def postGraphQL(url: str, headers: dict[str, str], query: str) -> dict | int:
    response: Response = post(url=url, headers=headers, json={"query": query})

    match response.status_code:
        case 404:
            return 404
        case 403:
            return 403
        case _:
            return loads(s=response.content)
