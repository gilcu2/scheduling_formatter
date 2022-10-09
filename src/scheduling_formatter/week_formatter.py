from enum import Enum
from typing import Dict
from scheduling_formatter.day_formatter import Day_Scheduling, format_day, check_day
from option import Result, Ok, Err


class WeekDays(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


day_list = [day for day in WeekDays]
next_day = {day_list[i]: day_list[i + 1] for i in range(len(day_list) - 1)}
next_day[day_list[len(day_list) - 1]] = day_list[0]

Week_Scheduling = Dict[WeekDays, Day_Scheduling]

opening_line = "A restaurant is open:\n"


def fix(scheduling: Week_Scheduling) -> Week_Scheduling:
    return scheduling


def check(scheduling: Week_Scheduling) -> Result[None, str]:
    for day in WeekDays:
        check_day_result = check_day(scheduling[day], scheduling[next_day[day]])
        if check_day_result.is_err:
            return check_day_result
    return Ok(None)


def format_from_formatted_days(formatted_days: Dict[WeekDays, str]) -> str:
    accumulator = opening_line
    for day in WeekDays:
        accumulator += f"{formatted_days[day]}\n"

    return accumulator


def format_from_scheduling(scheduling: Week_Scheduling) -> Result[str, str]:
    fixed_scheduling = fix(scheduling)
    check_result = check(fixed_scheduling)

    if check_result.is_err:
        Err(check_result.unwrap_err())

    formatted_days = {
        day: format_day(day_scheduling, scheduling[next_day[day]])
        for (day, day_scheduling) in scheduling.items()
    }

    return Ok(format_from_formatted_days(formatted_days))
