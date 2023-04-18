from json import loads

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from requests import Response, get, post

from prime_issues.utils.config import Config
from prime_issues.utils.types.jsonSchema import responseSchema


def checkURL(url: str) -> bool:
    responseCode: int = get(url=url).status_code

    match responseCode:
        case 404:
            return False
        case _:
            return True


def postGraphQL(
    url: str, headers: dict[str, str], query: str, config: Config
) -> dict | int:
    response: Response = post(url=url, headers=headers, json={"query": query})

    match response.status_code:
        case 404:
            return 404
        case 403:
            return 403
        case _:
            json: dict = loads(s=response.content)
            try:
                validate(instance=json, schema=responseSchema)
            except ValidationError:
                config.LOGGER.info(
                    msg=f"Returned JSON does not match JSONSchema. Data: {response.content.decode()}"
                )
                exit()
            else:
                return json
