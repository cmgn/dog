import enum

from typing import Tuple


class TokenType(enum.Enum):
    INTEGER = 0
    FLOAT = 1
    SYMBOL = 2
    LEFT_BRACKET = 3
    RIGHT_BRACKET = 4
    QUOTE = 5


Token = Tuple[TokenType, str]
