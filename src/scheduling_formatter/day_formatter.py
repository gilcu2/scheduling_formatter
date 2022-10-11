from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from option import Result, Ok, Err
from scheduling_formatter.time_formatter import format_time


class ActionType(str, Enum):
    open = "open"
    close = "close"


class Action(BaseModel):
    type: ActionType
    value: int = Field(ge=0, le=86399, description="The value are the seconds from midnight. Valid range [0,86399]")

    def __init__(self, type: ActionType, value: int):
        super().__init__(type=type, value=value)


Day_Scheduling = List[Action]

closed_phrase = "Closed"


def check_day(current_day_scheduling: Day_Scheduling, next_day_scheduling: Optional[Day_Scheduling] = None,
              previous_day_scheduling: Optional[Day_Scheduling] = None) -> Result[None, str]:
    def check_begin() -> bool:
        return current_day_scheduling[0].type == ActionType.open or \
               (len(previous_day_scheduling) > 0 and previous_day_scheduling[-1].type == ActionType.open)

    def check_end() -> bool:
        return current_day_scheduling[-1].type == ActionType.close or \
               (len(next_day_scheduling) > 0 and next_day_scheduling[0].type == ActionType.close)

    def check_sequence() -> Result[None, str]:
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

    if current_day_scheduling is None or len(current_day_scheduling) == 0:
        return Ok(None)

    if next_day_scheduling is None:
        next_day_scheduling = []

    if previous_day_scheduling is None:
        previous_day_scheduling = []

    if not check_begin():
        return Err(f"Day can not begin with close {current_day_scheduling[0]} if previous doesn't finish with open")

    if not check_end():
        return Err(f"Day can not finish with open {current_day_scheduling[-1]} if next doesn't begin with close")

    return check_sequence()


def format_day(current_day_scheduling: Day_Scheduling, next_day_scheduling: Optional[Day_Scheduling] = None,
               previous_day_scheduling: Optional[Day_Scheduling] = None) -> Result[str, str]:
    def format_pair(first: Action, second: Action) -> str:
        return f"{format_time(first.value)} - {format_time(second.value)}"

    check_result = check_day(current_day_scheduling, next_day_scheduling, previous_day_scheduling)
    if check_result.is_err:
        return Err(check_result.unwrap_err())

    if current_day_scheduling is None or len(current_day_scheduling) == 0:
        return Ok(closed_phrase)

    if len(current_day_scheduling) == 1 and current_day_scheduling[0].type == ActionType.close:
        return Ok(closed_phrase)

    current_day_clean_scheduling = current_day_scheduling \
        if current_day_scheduling[0].type == ActionType.open else current_day_scheduling[1:]

    if len(current_day_clean_scheduling) == 0:
        return Ok(closed_phrase)

    formatted = ""
    for i in range(0, len(current_day_clean_scheduling)-1, 2):
        formatted += format_pair(current_day_clean_scheduling[i], current_day_clean_scheduling[i + 1])
        if len(current_day_scheduling) > i + 2:
            formatted += ", "

    if len(current_day_clean_scheduling) % 2 != 0:
        formatted += format_pair(current_day_clean_scheduling[-1], next_day_scheduling[0])

    return Ok(formatted)
