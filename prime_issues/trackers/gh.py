from progress.bar import Bar

from prime_issues import trackers
from prime_issues.utils import network
from prime_issues.utils.config import Config
from typing import List
from pandas import DataFrame

def main(config: Config) -> None:
    githubURL: str = f"https://github.com/{config.AUTHOR}/{config.REPO_NAME}"

    if network.checkURL(url=githubURL) is False:
        config.LOGGER.info(msg=f"{githubURL} is not a valid GitHub URL.")
        exit(1)

    headers: dict[str:str] = {
        "Content-Type": "application/json",
        "Authorization": "bearer " + config.TOKEN,
    }

    baseQuery: str = trackers.ghGraphQLQuery.replace("$AUTHOR", f'"{config.AUTHOR}"').replace(
        "$REPO", f'"{config.REPO_NAME}"'
    )

    CURSOR: str = "null"
    MESSAGE: str = f"Getting issues from {githubURL}..."
    with Bar(message=MESSAGE, max=100) as bar:
        while True:
            query = baseQuery.replace("$CURSOR", CURSOR)

            response: dict | int = network.postGraphQL(
                url="https://api.github.com/graphql", headers=headers, query=query, config=config
            )

            if type(response) is int:
                config.LOGGER.info(msg=f"Error getting data. Code {response}")
                exit(1)

            rateLimitData: dict = response["data"]["rateLimit"]
            remainingCalls: int = rateLimitData["remaining"]
            resetTime: str = rateLimitData["resetAt"]

            issuesData:dict = response["data"]["repository"]["issues"]
            totalNumberOfCalls: int = round(issuesData["totalCount"] / 100)

            nodes: List[dict] = issuesData["nodes"]
            nodesDF: DataFrame = DataFrame(data=nodes)
            config.DF_LIST.append(nodesDF)

            MESSAGE = f"Getting issues from {githubURL} (Remaining calls: {remainingCalls})... "
            bar.max = totalNumberOfCalls
            bar.message = MESSAGE

            bar.update()
            bar.next()

            pageInfoData: dict = issuesData["pageInfo"]
            if pageInfoData["hasNextPage"]:
                CURSOR = f'"{pageInfoData["endCursor"]}"'
            else:
                break
