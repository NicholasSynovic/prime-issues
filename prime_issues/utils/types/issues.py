import numpy
from typedframe import TypedDataFrame


class Issues(TypedDataFrame):
    schema: dict = {
        "id": str,
        "Status": str,
        "CreatedAt": numpy.int16,
        "ClosedAt": numpy.int16,
    }
