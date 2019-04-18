from src.parser import parse
from src.tokens import TokenType


def test_unclosed_brackets():
    tests = (
        [(TokenType.LEFT_BRACKET, "(")],
        [
            (TokenType.LEFT_BRACKET, "("),
            (TokenType.LEFT_BRACKET, "("),
            (TokenType.RIGHT_BRACKET, ")"),
        ],
    )
    for test in tests:
        try:
            parse(test)
        except ValueError:
            continue
        assert False, str(test) + " should throw a ValueError"


def test_stray_right_bracket():
    tests = (
        [
            (TokenType.LEFT_BRACKET, "("),
            (TokenType.RIGHT_BRACKET, ")"),
            (TokenType.RIGHT_BRACKET, ")"),
        ],
    )
    for test in tests:
        try:
            parse(test)
        except ValueError:
            continue
        assert False, str(test) + " should throw a ValueError"


def test_empty_token_list():
    assert parse([]) == []


def test_parse_trivial_tokens():
    tests = (
        ((TokenType.INTEGER, "5"), 5),
        ((TokenType.SYMBOL, "abc"), "abc"),
        ((TokenType.FLOAT, "5.0"), 5.0),
    )
    for given, expected in tests:
        assert parse([given]) == [expected]


def test_parse_nonnested_lists():
    tests = (
        (
            [
                (TokenType.LEFT_BRACKET, "("),
                (TokenType.SYMBOL, "abc"),
                (TokenType.RIGHT_BRACKET, ")"),
            ],
            ("abc",),
        ),
        (
            [
                (TokenType.LEFT_BRACKET, "("),
                (TokenType.INTEGER, "123"),
                (TokenType.SYMBOL, "abc"),
                (TokenType.RIGHT_BRACKET, ")"),
            ],
            (123, "abc"),
        ),
    )
    for given, expected in tests:
        assert parse(given) == [expected]


def test_parse_nested_lists():
    tests = (
        (
            [
                (TokenType.LEFT_BRACKET, "("),
                (TokenType.LEFT_BRACKET, "("),
                (TokenType.SYMBOL, "abc"),
                (TokenType.RIGHT_BRACKET, ")"),
                (TokenType.INTEGER, "123"),
                (TokenType.LEFT_BRACKET, "("),
                (TokenType.FLOAT, "123.0"),
                (TokenType.RIGHT_BRACKET, ")"),
                (TokenType.RIGHT_BRACKET, ")"),
            ],
            (("abc",), 123, (123.0,)),
        ),
    )
    for given, expected in tests:
        assert parse(given) == [expected]


def test_parse_empty_lists():
    tests = (
        (
            [
                (TokenType.LEFT_BRACKET, "("),
                (TokenType.LEFT_BRACKET, "("),
                (TokenType.LEFT_BRACKET, "("),
                (TokenType.RIGHT_BRACKET, ")"),
                (TokenType.RIGHT_BRACKET, ")"),
                (TokenType.RIGHT_BRACKET, ")"),
            ],
            (((),),),
        ),
    )
    for given, expected in tests:
        assert parse(given) == [expected]
