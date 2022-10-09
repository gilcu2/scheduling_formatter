from scheduling_formatter.day_formatter import check_day_scheduling, Action, \
    ActionType


def test_1_open_close():
    # Given good scheduling
    scheduling = [
        Action(ActionType.open, 9 * 3600),
        Action(ActionType.close, 21 * 3600),
    ]

    # When check
    r = check_day_scheduling(scheduling)

    # Then it must be ok
    assert r.is_ok
