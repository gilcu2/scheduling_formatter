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

WeekScheduling = Dict[WeekDays, Day_Scheduling]

opening_line = "A restaurant is open:\n"


def format_from_formatted_days(formatted_days: Dict[WeekDays, str]) -> str:
    accumulator = opening_line
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
