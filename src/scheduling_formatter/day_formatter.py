from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from option import Result, Ok, Err



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


def check_day_scheduling(current_day_scheduling: Day_Scheduling, next_day_scheduling: Optional[Day_Scheduling] = None,
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

    if len(current_day_scheduling) == 0:
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



def format_day(current_day_scheduling: Day_Scheduling, next_day_scheduling: Day_Scheduling) -> str:
    if len(current_day_scheduling) == 0:
        return closed_phrase

    if len(current_day_scheduling) == 1 and current_day_scheduling[0].type == ActionType.close:
        return closed_phrase

    return ""
