from requests import Response, get, post


def checkURL(url: str) -> bool:
    responseCode: int = get(url=url).status_code

    match responseCode:
        case 404:
            return False
        case _:
            return True


def postGraphQL(url: str, headers: dict[str, str], query: str) -> None:
    response: Response = post(url=url, headers=headers, data=query)
    print(response.content)
