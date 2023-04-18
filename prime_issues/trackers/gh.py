from prime_issues import trackers
from prime_issues.utils import network
from prime_issues.utils.config import Config


def main(config: Config) -> None:
    githubURL: str = f"https://github.com/{config.AUTHOR}/{config.REPO_NAME}"

    if network.checkURL(url=githubURL) is False:
        config.LOGGER.info(msg=f"{githubURL} is not a valid GitHub URL.")
        exit(1)

    headers: dict[str:str] = {
        "Content-Type": "application/json",
        "Authorization": "bearer " + config.TOKEN,
    }

    response: dict | int = network.postGraphQL(
        url="https://api.github.com/graphql", headers=headers, query=query
    )

    if type(response) is int:
        config.LOGGER.info(msg=f"Error getting data. Code {response}")
        exit(1)

    import pprint

    pprint.pprint(response)
