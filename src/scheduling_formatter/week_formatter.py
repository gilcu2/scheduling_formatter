from enum import Enum
from typing import Dict
from scheduling_formatter.day_formatter import Day_Scheduling, format_day, check_day, closed_phrase
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
next_day[day_list[-1]] = day_list[0]

previous_day = {day_list[i]: day_list[i - 1] for i in range(1, len(day_list))}
previous_day[day_list[0]] = day_list[-1]

Week_Scheduling = Dict[WeekDays, Day_Scheduling]

opening_line = "A restaurant is open:\n"


def check_week(scheduling: Week_Scheduling) -> Result[None, str]:
    for day in WeekDays:
        check_day_result = check_day(scheduling.get(day), scheduling.get(next_day[day]),
                                     scheduling.get(previous_day[day]))
        if check_day_result.is_err:
            return check_day_result
    return Ok(None)


def format_from_formatted_days(formatted_days: Dict[WeekDays, str]) -> str:
    accumulator = opening_line
    for day in WeekDays:
        if day in formatted_days:
            accumulator += f"{formatted_days[day]}\n"
        else:
            accumulator += f"{day.capitalize()}: {closed_phrase}\n"

    return accumulator


def format_week(scheduling: Week_Scheduling) -> Result[str, str]:
    check_result = check_week(scheduling)

    if check_result.is_err:
        Err(check_result.unwrap_err())

    formatted_days = {
        day: format_day(day_scheduling, scheduling[next_day[day]])
        for (day, day_scheduling) in scheduling.items()
    }

    return Ok(format_from_formatted_days(formatted_days))
