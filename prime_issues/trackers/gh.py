from typing import List

import pandas
from pandas import DataFrame
from progress.bar import Bar

from prime_issues import trackers
from prime_issues.utils import network
from prime_issues.utils.config import Config


def main(config: Config) -> None:
    githubURL: str = f"https://github.com/{config.AUTHOR}/{config.REPO_NAME}"

    if network.checkURL(url=githubURL) is False:
        config.LOGGER.info(msg=f"{githubURL} is not a valid GitHub URL.")
        exit(1)

    HEADERS: dict[str:str] = {
        "Content-Type": "application/json",
        "Authorization": "bearer " + config.TOKEN,
    }
    URL: str = "https://api.github.com/graphql"
    CURSOR: str = "null"
    MESSAGE: str = f"Getting issues from {githubURL}..."

    baseQuery: str = trackers.ghGraphQLQuery.replace(
        "$AUTHOR", f'"{config.AUTHOR}"'
    ).replace("$REPO", f'"{config.REPO_NAME}"')

    with Bar(message=MESSAGE, max=100) as bar:
        while True:
            query = baseQuery.replace("$CURSOR", CURSOR)

            config.LOGGER.info(msg=f"Sending POST request to: {URL}")
            config.LOGGER.info(msg=f"POST headers: {HEADERS}")
            config.LOGGER.info(msg=f"POST JSON: {query}")

            response: dict | int = network.postGraphQL(
                url=URL,
                headers=HEADERS,
                query=query,
                config=config,
            )

            if type(response) is int:
                config.LOGGER.info(msg=f"Error getting data. Code {response}")
                exit(1)

            rateLimitData: dict = response["data"]["rateLimit"]
            remainingCalls: int = rateLimitData["remaining"]
            resetTime: str = rateLimitData["resetAt"]

            issuesData: dict = response["data"]["repository"]["issues"]
            totalNumberOfCalls: int = round(issuesData["totalCount"] / 100)

            nodes: List[dict] = issuesData["nodes"]
            nodesDF: DataFrame = DataFrame(data=nodes)
            config.DF_LIST.append(nodesDF)

            MESSAGE = f"Getting issues from {githubURL} (Remaining calls: {remainingCalls})... "
            bar.max = totalNumberOfCalls
            bar.message = MESSAGE

            bar.update()
            bar.next()

            config.LOGGER.info(msg=f"Remaining GraphQL calls: {remainingCalls}")
            config.LOGGER.info(msg=f"GraphQL reset time: {resetTime}")
            config.LOGGER.info(
                msg=f"Total number of GraphQL calls: {totalNumberOfCalls}"
            )

            pageInfoData: dict = issuesData["pageInfo"]
            if pageInfoData["hasNextPage"]:
                CURSOR = f'"{pageInfoData["endCursor"]}"'
            else:
                break

    df: DataFrame = pandas.concat(objs=config.DF_LIST, ignore_index=True)
    df.T.to_json(path_or_buf=config.OUTPUT, indent=4)
