from json import loads

responseSchemaStr: str = """{
    "$schema": "http://json-schema.org/draft-06/schema#",
    "$ref": "#/definitions/IssueInformation",
    "definitions": {
        "IssueInformation": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "data": {
                    "$ref": "#/definitions/Data"
                }
            },
            "required": [
                "data"
            ],
            "title": "IssueInformation"
        },
        "Data": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "repository": {
                    "$ref": "#/definitions/Repository"
                },
                "rateLimit": {
                    "$ref": "#/definitions/RateLimit"
                }
            },
            "required": [
                "rateLimit",
                "repository"
            ],
            "title": "Data"
        },
        "RateLimit": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "limit": {
                    "type": "integer"
                },
                "cost": {
                    "type": "integer"
                },
                "remaining": {
                    "type": "integer"
                },
                "resetAt": {
                    "type": "string",
                    "format": "date-time"
                }
            },
            "required": [
                "cost",
                "limit",
                "remaining",
                "resetAt"
            ],
            "title": "RateLimit"
        },
        "Repository": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "issues": {
                    "$ref": "#/definitions/Issues"
                }
            },
            "required": [
                "issues"
            ],
            "title": "Repository"
        },
        "Issues": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "totalCount": {
                    "type": "integer"
                },
                "nodes": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Node"
                    }
                },
                "pageInfo": {
                    "$ref": "#/definitions/PageInfo"
                }
            },
            "required": [
                "nodes",
                "pageInfo",
                "totalCount"
            ],
            "title": "Issues"
        },
        "Node": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "id": {
                    "type": "string"
                },
                "state": {
                    "type": "string"
                },
                "createdAt": {
                    "type": "string",
                    "format": "date-time"
                },
                "closedAt": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "date-time"
                        },
                        {
                            "type": "null"
                        }
                    ]
                }
            },
            "required": [
                "closedAt",
                "createdAt",
                "id",
                "state"
            ],
            "title": "Node"
        },
        "PageInfo": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "endCursor": {
                    "type": "string"
                },
                "hasNextPage": {
                    "type": "boolean"
                }
            },
            "required": [
                "endCursor",
                "hasNextPage"
            ],
            "title": "PageInfo"
        }
    }
}
"""

outputIssuesSchemaStr: str = """{
    "$schema": "http://json-schema.org/draft-06/schema#",
    "type": "object",
    "additionalProperties": {
        "$ref": "#/definitions/OutputIssuesInformationValue"
    },
    "definitions": {
        "OutputIssuesInformationValue": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "id": {
                    "type": "string"
                },
                "state": {
                    "type": "string"
                },
                "createdAt": {
                    "type": "string",
                    "format": "date-time"
                },
                "closedAt": {
                    "anyOf": [
                        {
                            "type": "string",
                            "format": "date-time"
                        },
                        {
                            "type": "null"
                        }
                    ]
                }
            },
            "required": [
                "closedAt",
                "createdAt",
                "id",
                "state"
            ],
            "title": "OutputIssuesInformationValue"
        }
    }
}
"""

responseSchema: dict = loads(s=responseSchemaStr)
outputIssuesSchema: dict = loads(s=outputIssuesSchemaStr)
