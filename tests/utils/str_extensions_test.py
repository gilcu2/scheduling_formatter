from utils.str_extensions import clean


def test_clean() -> None:
    # Given str extra formatting chars
    s = """
            Monday: 9 AM - 8 PM
            Tuesday: 10 AM - 1 PM
    """

    # And the expected cleaned str
    cleaned = """
Monday: 9 AM - 8 PM
Tuesday: 10 AM - 1 PM
""".strip()

    # When cleaned
    r = clean(s)

    # Then result is the expected
    assert r == cleaned
