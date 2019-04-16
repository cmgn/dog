import src.tokens as tokens

from typing import List, Callable, Dict


CharPredicate = Callable[[str], bool]


def scan_predicate(string: str, predicate: CharPredicate, position: int = 0):
    """
    Get the largest prefix of a string that satisfies a predicate.

    Input:
        string - the string.
        predicate - the predicate, this is called on each character.
    Output:
        string - the prefix.
        position - the new position.
    """
    start = position
    while position < len(string) and predicate(string[position]):
        position += 1
    return string[start:position], position


def scan_integer(string: str, position: int = 0):
    """
    Scan an integer from a string.

    Input:
        string - the string.
        position - the starting position.
    Output:
        token - the integer token.
        position - the new position.
    Raises:
        ValueError - if the token is invalid.
    """
    extract, position = scan_predicate(string, str.isdigit, position)
    # This is to make sure that we reject literals such as '5z'.
    if position < len(string) and string[position].isalnum():
        raise ValueError(
            "scan error: invalid token {}".format(extract + string[position])
        )
    return (tokens.TokenType.INTEGER, extract), position


def scan_symbol(string: str, position: int = 0):
    """
    Scan a symbol from a string.

    Input:
        string - the string.
        position - the starting position.
    Output:
        token - the symbol token.
        position - the new position.
    """
    extract, position = scan_predicate(string, str.isalnum, position)
    return (tokens.TokenType.SYMBOL, extract), position


CONSTANT_TOKENS: Dict[str, tokens.Token] = {
    "(": (tokens.TokenType.LEFT_BRACKET, "("),
    ")": (tokens.TokenType.RIGHT_BRACKET, ")"),
}


def scan(string: str, starting_position: int = 0) -> List[tokens.Token]:
    """
    Scan a list of tokens from a string. The token types are as
    documented in the standard.

    Input:
        string - the string.
        [starting_position] - the starting position in the string.
    Output:
        List[token.Token] - the list of tokens.
    Raises:
        ValueError - if the input stream is syntactically incorrect.
    """
    output_tokens = []
    position = starting_position
    while position < len(string):
        char = string[position]
        if char.isspace():
            position += 1
            continue
        # Starting position of the current token.
        if char.isdigit():
            token, position = scan_integer(string, position)
        elif char.isalnum():
            token, position = scan_symbol(string, position)
        elif char in CONSTANT_TOKENS:
            # For now only single character constant tokens exist, so
            # this method is fine.
            token = CONSTANT_TOKENS[char]
            position += len(token[1])
        else:
            # TODO(cmgn): better error message here
            raise ValueError("invalid character: {}".format(string[position]))
        output_tokens.append(token)
    return output_tokens
