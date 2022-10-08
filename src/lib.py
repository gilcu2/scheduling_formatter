from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, List
from datetime import datetime
from option import Result, Ok, Err


class WeekDay(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class ActionType(str, Enum):
    open = "open"
    close = "close"


class Action(BaseModel):
    type: ActionType
    value: int = Field(ge=0, le=86399, description="The value are the seconds from midnight. Valid range [0,86399]")


Scheduling = Dict[WeekDay, List[Action]]


async def format(scheduling: Scheduling) -> Result[str, str]:
    s = "A restaurant is open:\n"
    for day in WeekDay:
        if day in scheduling:
            day_line = f"{day}:"
            for action in scheduling[day]:
                separator = " "
                time_str = datetime.fromtimestamp(action.value).strftime("%I:%M:%S %p")
                if action.type == ActionType.open:
                    day_line += f"{separator}{time_str}"
                else:
                    day_line += f" - {time_str}"
                separator = ", "
        else:
            day_line = f"{day}: Closed"
        s += f"{day_line}\n"

    return Ok(s)
