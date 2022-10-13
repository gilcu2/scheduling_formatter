from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from option import Result, Ok, Err
from scheduling_formatter.time_formatter import format_time
import logging


class ActionType(str, Enum):
    open = "open"
    close = "close"


@dataclass
class Action:
    type: ActionType
    value: int

    def __post_init__(self):
        assert self.value < 24 * 3600


Day_Scheduling = List[Action]

closed_phrase = "Closed"


def _check_day(current_day_scheduling: Day_Scheduling, next_day_scheduling: Day_Scheduling,
               previous_day_scheduling: Day_Scheduling) -> Result[None, str]:
    def check_begin() -> bool:
        return current_day_scheduling[0].type == ActionType.open or (
            len(previous_day_scheduling) > 0 and previous_day_scheduling[-1].type == ActionType.open
        )

    def check_end() -> bool:
        return current_day_scheduling[-1].type == ActionType.close or (
            len(next_day_scheduling) > 0 and next_day_scheduling[0].type == ActionType.close
        )

    if len(current_day_scheduling) == 0:
        return Ok(None)

    if not check_begin():
        return Err(f"Day can not begin with close {current_day_scheduling[0]} if previous doesn't finish with open")

    if not check_end():
        return Err(f"Day can not finish with open {current_day_scheduling[-1]} if next doesn't begin with close")

    previous_time = current_day_scheduling[0].value
    previous_type = current_day_scheduling[0].type
    for action in current_day_scheduling[1:]:
        if action.value <= previous_time:
            return Err(f"Action {action} must be after previous")
        if action.type == previous_type:
            return Err(f"Action {action} can not be the same type than previous")
        previous_time = action.value
        previous_type = action.type
    return Ok(None)


def check_day(current_day_scheduling: Day_Scheduling, next_day_scheduling: Optional[Day_Scheduling] = None,
              previous_day_scheduling: Optional[Day_Scheduling] = None) -> Result[None, str]:
    if next_day_scheduling is None:
        next_day_scheduling = []

    if previous_day_scheduling is None:
        previous_day_scheduling = []

    r = _check_day(current_day_scheduling, next_day_scheduling, previous_day_scheduling)
    if r.is_err:
        logging.warning(r.unwrap_err())
    return r


def format_day(current_day_scheduling: Optional[Day_Scheduling], next_day_scheduling: Optional[Day_Scheduling] = None,
               previous_day_scheduling: Optional[Day_Scheduling] = None) -> Result[str, str]:
    def format_pair(first: Action, second: Action) -> str:
        return f"{format_time(first.value)} - {format_time(second.value)}"

    current_day_scheduling = current_day_scheduling if current_day_scheduling is not None else []
    next_day_scheduling = next_day_scheduling if next_day_scheduling is not None else []
    next_day_scheduling = next_day_scheduling if next_day_scheduling is not None else []

    check_result = check_day(current_day_scheduling, next_day_scheduling, previous_day_scheduling)
    if check_result.is_err:
        return Err(check_result.unwrap_err())

    if len(current_day_scheduling) == 0:
        return Ok(closed_phrase)

    if len(current_day_scheduling) == 1 and current_day_scheduling[0].type == ActionType.close:
        return Ok(closed_phrase)

    current_day_clean_scheduling = current_day_scheduling \
        if current_day_scheduling[0].type == ActionType.open else current_day_scheduling[1:]

    if len(current_day_clean_scheduling) == 0:
        return Ok(closed_phrase)

    formatted = ""
    for i in range(0, len(current_day_clean_scheduling) - 1, 2):
        formatted += format_pair(current_day_clean_scheduling[i], current_day_clean_scheduling[i + 1])
        if len(current_day_clean_scheduling) > i + 2:
            formatted += ", "

    if len(current_day_clean_scheduling) % 2 != 0:
        formatted += format_pair(current_day_clean_scheduling[-1], next_day_scheduling[0])

    return Ok(formatted)
