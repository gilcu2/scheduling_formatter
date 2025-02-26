import pytest

from scheduling_formatter.day_formatter import Action, ActionType


def test_action_good_input():
    # Given action type and seconds
    action_type = ActionType.open
    seconds = 3600

    # When create
    action = Action(type=action_type, value=seconds)

    # Then must be ok
    assert action


def test_action_bad_input_seconds():
    # Given action type and seconds
    action_type = ActionType.open
    seconds = 100000

    # When create must generate exception
    with pytest.raises(AssertionError):
        Action(type=action_type, value=seconds)
