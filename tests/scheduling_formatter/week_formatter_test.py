from scheduling_formatter.week_formatter import \
    format_week, format_from_formatted_days, WeekDays, WeekSchedulingPydantic
from scheduling_formatter.day_formatter import Action, ActionType
from utils.str_extensions import clean


def test_format_from_formatted_days():
    # Given formatted days
    formatted_days = {WeekDays.monday: "9 AM - 8 PM"}

    # And the expected formatted
    expected = clean("""
            Monday: 9 AM - 8 PM
            Tuesday: Closed
            Wednesday: Closed
            Thursday: Closed
            Friday: Closed
            Saturday: Closed
            Sunday: Closed
    """)

    # When format
    formatted = format_from_formatted_days(formatted_days).strip()

    # Then results is the expected
    assert formatted == expected


def test_format_week():
    # Given a scheduling
    scheduling = {
        WeekDays.monday: [
            Action(type=ActionType.open, value=9 * 3600),
            Action(type=ActionType.close, value=20 * 3600),
        ],
    }

    # And the expected result
    expected = format_from_formatted_days({WeekDays.monday: "9 AM - 8 PM"})

    # When format it
    r = format_week(scheduling).unwrap()

    # Then r is the expected
    assert r == expected


def test_to_week_scheduling():
    # Given WeekSchedulingPydantic
    scheduling_pydantic = WeekSchedulingPydantic(monday=[
        Action(ActionType.open, 3600),
        Action(ActionType.close, 7200),
    ])

    # And the expected WeekScheduling
    expected = {
        "monday": [
            Action(ActionType.open, 3600),
            Action(ActionType.close, 7200),
        ]
    }

    # When converted
    converted = scheduling_pydantic.to_week_scheduling()

    # Then it is the expected
    assert converted == expected
