import src.tokens as tokens

from typing import List, Union, Tuple, Set

Expression = Union[int, float, str, Tuple["Expression", ...]]
Tokens = List[tokens.Token]


def _parse_list(toks: Tokens, position: int = 0) -> Tuple[Expression, int]:
    # Skip the opening bracket
    position += 1
    expressions = []
    while position < len(toks):
        typ, _ = toks[position]
        # We should terminate upon finding a right bracket. I tried putting
        # this in the while loop's condition but it was very ugly.
        if typ == tokens.TokenType.RIGHT_BRACKET:
            break
        expression, position = _parse(toks, position)
        expressions.append(expression)
    if position >= len(toks):
        raise ValueError("unclosed brackets")
    # We add one to skip the right bracket.
    return tuple(expressions), position + 1


def _parse(toks: Tokens, position: int) -> Tuple[Expression, int]:
    typ, val = toks[position]
    if typ == tokens.TokenType.INTEGER:
        return int(val), position + 1
    elif typ == tokens.TokenType.FLOAT:
        return float(val), position + 1
    elif typ == tokens.TokenType.SYMBOL:
        return val, position + 1
    elif typ == tokens.TokenType.LEFT_BRACKET:
        return _parse_list(toks, position)
    raise ValueError(toks[position])


def parse(toks: List[tokens.Token], position: int = 0) -> List[Expression]:
    """
    Parse a list of tokens into a list of expressions.

    Input:
        toks - the list of tokens.
        position [optional] - the starting index inside of tokens.
    Output:
        expressions - the list of expressions.
    Raises:
        ValueError - syntax errors in the input.
    """
    expressions = []
    while position < len(toks):
        expression, position = _parse(toks, position)
        expressions.append(expression)
    return expressions
