from datetime import datetime


def format_time(seconds: int) -> str:
    time = datetime.utcfromtimestamp(seconds)
    if time.second != 0:
        return time.strftime("%-I:%M:%S %p")
    if time.minute != 0:
        return time.strftime("%-I:%M %p")
    return time.strftime("%-I %p")
