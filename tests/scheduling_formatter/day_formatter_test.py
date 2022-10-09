import pytest

from scheduling_formatter.day_formatter import Action, ActionType


def test_Action_good_input():
    # Given action type and seconds
    action_type = ActionType.open
    seconds = 3600

    # When create
    action = Action(type=action_type, value=seconds)

    # Then must be ok
    assert action


def test_Action_bad_input_seconds():
    # Given action type and seconds
    action_type = ActionType.open
    seconds = 100000

    # When create must generate exception
    with pytest.raises(Exception) as e_info:
        action = Action(type=action_type, value=seconds)


def test_Action_bad_input_action_type():
    # Given action type and seconds
    action_type = "run"
    seconds = 10000

    # When create must generate exception
    with pytest.raises(Exception) as e_info:
        action = Action(type=action_type, value=seconds)
