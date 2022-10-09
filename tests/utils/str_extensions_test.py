from utils.str_extensions import clean


def test_clean():
    # Given str extra formatting chars
    s = """
            A restaurant is open:
            Monday: 9 AM - 8 PM
    """

    # And the expected cleaned str
    cleaned = """
A restaurant is open:
Monday: 9 AM - 8 PM
""".strip()

    # When cleaned
    r = clean(s)

    # Then result is the expected
    assert r == cleaned
