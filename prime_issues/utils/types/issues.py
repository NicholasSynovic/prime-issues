import numpy
from typedframe import TypedDataFrame

class Issues(TypedDataFrame):
    schema: dict = {
        "id": str,
        "State": str,
        "CreatedAt": numpy.int64,
        "ClosedAt": numpy.int64,
    }
