from lib import WeekDay, ActionType, Action, format
import pytest


@pytest.mark.asyncio
async def test_format():
    # Given a scheduling
    scheduling = {
        WeekDay.monday: [
            Action(type=ActionType.open, value=32400),
            Action(type=ActionType.open, value=32400),
        ],
    }

    # And the expected result
    expected = """
        A restaurant is open:
        Monday: 9 AM - 8 PM
    """.strip()

    # When format it
    r = (await format(scheduling)).unwrap()

    # Then r is the expected
    assert r == expected
