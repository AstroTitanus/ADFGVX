from enum import Enum

class Mode(Enum):
    SK = 1
    CZ = 2
    LONG = 3

class Type(Enum):
    ENCRYPT = 1
    DECRYPT = 2
    PASSWORD = 3