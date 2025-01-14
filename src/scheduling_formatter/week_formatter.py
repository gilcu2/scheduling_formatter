from enum import Enum
from scheduling_formatter.day_formatter import Day_Scheduling, format_day, closed_phrase
from option import Result, Ok
from pydantic import BaseModel
from typing import Dict, Any, Optional, cast


class WeekDays(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


day_list = list(WeekDays)

next_day = {day_list[i]: day_list[i + 1] for i in range(len(day_list) - 1)}
next_day[day_list[-1]] = day_list[0]

previous_day = {day_list[i]: day_list[i - 1] for i in range(1, len(day_list))}
previous_day[day_list[0]] = day_list[-1]

WeekScheduling = Dict[WeekDays, Day_Scheduling]


def format_from_formatted_days(formatted_days: Dict[WeekDays, str]) -> str:
    accumulator = ""
    for day in WeekDays:
        if day in formatted_days:
            accumulator += f"{day.capitalize()}: {formatted_days[day]}\n"
        else:
            accumulator += f"{day.capitalize()}: {closed_phrase}\n"

    return accumulator


def format_week(scheduling: WeekScheduling) -> Result[str, str]:
    formatted_days: Dict[WeekDays, str] = {}
    for day in WeekDays:
        possible_formatted = format_day(scheduling.get(day), scheduling.get(next_day[day]),
                                        scheduling.get(previous_day[day]))
        if possible_formatted.is_err:
            return possible_formatted
        formatted_days[day] = possible_formatted.unwrap()

    return Ok(format_from_formatted_days(formatted_days))


class WeekSchedulingPydantic(BaseModel):
    monday: Optional[Day_Scheduling] = None
    tuesday: Optional[Day_Scheduling] = None
    wednesday: Optional[Day_Scheduling] = None
    thursday: Optional[Day_Scheduling] = None
    friday: Optional[Day_Scheduling] = None
    saturday: Optional[Day_Scheduling] = None
    sunday: Optional[Day_Scheduling] = None

    def to_week_scheduling(self) -> WeekScheduling:
        converted=dict(self)
        without_none={k: v for k, v in converted.items() if v is not None}
        return cast(WeekScheduling, without_none)
