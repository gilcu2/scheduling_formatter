from fastapi import FastAPI
from typing import Dict, List
from pydantic import BaseModel, Field
from enum import Enum
from dataclasses import dataclass

app = FastAPI()


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


@app.get("/hello")
async def hello() -> Dict[str, str]:
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def hello_parameters(name: str, number: int = 0) -> Dict[str, str]:
    return {"message": f"Hello {name}{number}"}


@app.post("/format_scheduling")
async def format_scheduling(scheduling: Scheduling) -> str:
    return f"{scheduling}"
