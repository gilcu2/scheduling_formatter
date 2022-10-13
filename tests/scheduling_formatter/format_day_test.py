from scheduling_formatter.day_formatter import format_day, Action, \
    ActionType


def test_1_open_close():
    # Given good scheduling
    scheduling = [
        Action(ActionType.open, 9 * 3600),
        Action(ActionType.close, 21 * 3600),
    ]

    # And the expected result
    expected = "9 AM - 9 PM"

    # When format
    r = format_day(scheduling).unwrap()

    # Then it must be the expected
    assert r == expected


def test_2_open_close():
    # Given good scheduling
    scheduling = [
        Action(ActionType.open, 9 * 3600),
        Action(ActionType.close, 14 * 3600),
        Action(ActionType.open, 18 * 3600),
        Action(ActionType.close, 22 * 3600),
    ]

    # And the expected result
    expected = "9 AM - 2 PM, 6 PM - 10 PM"

    # When check
    r = format_day(scheduling).unwrap()

    # Then it must be ok
    assert r == expected


def test_1_open():
    # Given bad scheduling
    scheduling = [
        Action(ActionType.open, 9 * 3600),
    ]

    # When format
    r = format_day(scheduling)

    # Then it must be error
    assert r.is_err


def test_1_open_next_day_closed():
    # Given good scheduling
    current_day_scheduling = [
        Action(ActionType.open, 18 * 3600),
    ]

    next_day_scheduling = [
        Action(ActionType.close, 3 * 3600),
    ]

    # And the expected result
    expected = "6 PM - 3 AM"

    # When check
    r = format_day(current_day_scheduling, next_day_scheduling).unwrap()

    # Then it must be ok
    assert r == expected


def test_2_open():
    # Given bad scheduling
    scheduling = [
        Action(ActionType.open, 9 * 3600),
        Action(ActionType.open, 18 * 3600),
        Action(ActionType.close, 22 * 3600),
    ]

    # When check
    r = format_day(scheduling)

    # Then it must be error
    assert r.is_err


def test_1_open_close_wrong_times():
    # Given good scheduling
    scheduling = [
        Action(ActionType.open, 19 * 3600),
        Action(ActionType.close, 18 * 3600),
    ]

    # When check
    r = format_day(scheduling)

    # Then it must be error
    assert r.is_err
