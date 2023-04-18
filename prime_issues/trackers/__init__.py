ghGraphQLQuery: str = """{
    repository(owner: $AUTHOR, name: $REPO) {
    issues(first: 100, after: $CURSOR) {
      totalCount
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
}"""
