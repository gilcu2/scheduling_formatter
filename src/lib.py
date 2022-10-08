from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, List


class WeekDay(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class ActionType(str, Enum):
    open: "open"
    close: "close"


class Action(BaseModel):
    type: ActionType
    value: int = Field(ge=0, le=86399, description="The value are the seconds from midnight. Valid range [0,86399]")


Scheduling = Dict[WeekDay, List[Action]]


async def format(scheduling: Scheduling):
    pass
