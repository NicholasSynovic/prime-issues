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

    query: str = """{
    repository(owner: "{}", name: "{}") {
    issues(first: 100) {
      nodes {
        id
        state
        createdAt
        closedAt
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}""".format(
        config.AUTHOR, config.REPO_NAME
    )

    response = network.postGraphQL(
        url="https://api.github.com/graphql", headers=headers, query=query
    )
