from json import loads

from requests import Response, get, post
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from prime_issues.utils.config import Config


def checkURL(url: str) -> bool:
    responseCode: int = get(url=url).status_code

    match responseCode:
        case 404:
            return False
        case _:
            return True


def postGraphQL(url: str, headers: dict[str, str], query: str, config: Config) -> dict | int:
    response: Response = post(url=url, headers=headers, json={"query": query})

    match response.status_code:
        case 404:
            return 404
        case 403:
            return 403
        case _:
            try:
                validate()
            except ValidationError:
                config.LOGGER.info(msg=f"Returned JSON does not match JSONSchema. Data: {response.content.decode()}")
                exit()
            else:
                return loads(s=response.content)
