from scheduling_formatter.day_formatter import check_day, Action, \
    ActionType


def test_1_open_close():
    # Given good scheduling
    scheduling = [
        Action(ActionType.open, 9 * 3600),
        Action(ActionType.close, 21 * 3600),
    ]

    # When check
    r = check_day(scheduling)

    # Then it must be ok
    assert r.is_ok


def test_2_open_close():
    # Given good scheduling
    scheduling = [
        Action(ActionType.open, 9 * 3600),
        Action(ActionType.close, 14 * 3600),
        Action(ActionType.open, 18 * 3600),
        Action(ActionType.close, 22 * 3600),
    ]

    # When check
    r = check_day(scheduling)

    # Then it must be ok
    assert r.is_ok


def test_1_open():
    # Given bad scheduling
    scheduling = [
        Action(ActionType.open, 9 * 3600),
    ]

    # When check
    r = check_day(scheduling)

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

    # When check
    r = check_day(current_day_scheduling, next_day_scheduling)

    # Then it must be ok
    assert r.is_ok


def test_2_open():
    # Given bad scheduling
    scheduling = [
        Action(ActionType.open, 9 * 3600),
        Action(ActionType.open, 18 * 3600),
        Action(ActionType.close, 22 * 3600),
    ]

    # When check
    r = check_day(scheduling)

    # Then it must be error
    assert r.is_err


def test_1_open_close_wrong_times():
    # Given good scheduling
    scheduling = [
        Action(ActionType.open, 19 * 3600),
        Action(ActionType.close, 18 * 3600),
    ]

    # When check
    r = check_day(scheduling)

    # Then it must be error
    assert r.is_err
