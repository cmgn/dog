from src.tokens import TokenType
from src.scanner import scan


def test_scanner_throws_error_on_bad_integer():
    tests = ("5abc", "4_", "59595a4949")
    for test in tests:
        try:
            scan(test)
        except ValueError:
            continue
        else:
            assert False, test + " must throw a ValueError"


def test_scanner_throws_error_on_invalid_char():
    tests = ("£", "$", "@")
    for test in tests:
        try:
            scan(test)
        except ValueError:
            continue
        else:
            assert False, test + " must throw a ValueError"


def test_scanner_on_special_symbol_characters():
    tests = ("?", "??", "is-alpha", "+", "-", "*", "/")
    for given in tests:
        assert scan(given) == [(TokenType.SYMBOL, given)]


def test_scanner_on_single_literals():
    tests = (
        ("123", (TokenType.INTEGER, "123")),
        ("abc", (TokenType.SYMBOL, "abc")),
        ("a53e", (TokenType.SYMBOL, "a53e")),
    )
    for given, expected in tests:
        assert scan(given) == [expected]


def test_scanner_on_compound_literals():
    tests = (
        (
            "123 abc 123",
            [
                (TokenType.INTEGER, "123"),
                (TokenType.SYMBOL, "abc"),
                (TokenType.INTEGER, "123"),
            ],
        ),
        (
            "abc 40 a3e2",
            [
                (TokenType.SYMBOL, "abc"),
                (TokenType.INTEGER, "40"),
                (TokenType.SYMBOL, "a3e2"),
            ],
        ),
    )
    for given, expected in tests:
        assert scan(given) == expected


def test_scanner_on_lists():
    tests = (
        ("()", [(TokenType.LEFT_BRACKET, "("), (TokenType.RIGHT_BRACKET, ")")]),
        ("(", [(TokenType.LEFT_BRACKET, "(")]),
        (")", [(TokenType.RIGHT_BRACKET, ")")]),
        (
            "()(())",
            [
                (TokenType.LEFT_BRACKET, "("),
                (TokenType.RIGHT_BRACKET, ")"),
                (TokenType.LEFT_BRACKET, "("),
                (TokenType.LEFT_BRACKET, "("),
                (TokenType.RIGHT_BRACKET, ")"),
                (TokenType.RIGHT_BRACKET, ")"),
            ],
        ),
        (
            "(abc(123)ghi)",
            [
                (TokenType.LEFT_BRACKET, "("),
                (TokenType.SYMBOL, "abc"),
                (TokenType.LEFT_BRACKET, "("),
                (TokenType.INTEGER, "123"),
                (TokenType.RIGHT_BRACKET, ")"),
                (TokenType.SYMBOL, "ghi"),
                (TokenType.RIGHT_BRACKET, ")"),
            ],
        ),
    )
    for given, expected in tests:
        assert scan(given) == expected
