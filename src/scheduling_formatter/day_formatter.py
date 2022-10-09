from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, List
from option import Result, Ok, Err


class ActionType(str, Enum):
    open = "open"
    close = "close"


class Action(BaseModel):
    type: ActionType
    value: int = Field(ge=0, le=86399, description="The value are the seconds from midnight. Valid range [0,86399]")


Day_Scheduling = List[Action]

closed_phrase = "Closed"


def fix_day(day: Day_Scheduling, next_day: Day_Scheduling) -> Day_Scheduling:
    return day

def check_day(day: Day_Scheduling, next_day: Day_Scheduling) -> Result[None,str]:
    return Ok(None)

def format_day(day: Day_Scheduling, next_day: Day_Scheduling) -> str:
    return ""
