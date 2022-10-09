from scheduling_formatter.week_formatter import \
    format_from_scheduling, format_from_formatted_days, WeekDays
from scheduling_formatter.day_formatter import Action, ActionType


def test_format_from_formatted_days():
    # Given formatted days
    formatted_days = {WeekDays.monday: "Monday: 9 AM - 8 PM"}

    # And the expected formatted
    expected = """
            A restaurant is open:
            Monday: 9 AM - 8 PM
            Tuesday: Closed
            wednesday: Closed
            thursday: Closed
            Tuesday: Closed
            Tuesday: Closed
            Tuesday: Closed
        """.strip()

    # When format
    formatted = format_from_formatted_days(formatted_days)

    # Then results is the expected
    assert formatted == expected


def test_format():
    # Given a scheduling
    scheduling = {
        WeekDays.monday: [
            Action(type=ActionType.open, value=32400),
            Action(type=ActionType.open, value=32400),
        ],
    }

    # And the expected result
    expected = format_from_formatted_days({WeekDays.monday: "Monday: 9 AM - 8 PM"})

    # When format it
    r = format_from_scheduling(scheduling).unwrap()

    # Then r is the expected
    assert r == expected
