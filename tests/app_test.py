from fastapi.testclient import TestClient
from app import app
from scheduling_formatter.week_formatter import WeekDays, format_from_formatted_days
from utils.str_extensions import clean

client = TestClient(app)


def test_any_get() -> None:
    # Given the hello path
    path = "qq"

    # And the expected response
    expected_msg = "Undefined request"

    # When call the app
    response = client.get(f"/{path}")

    # Then response must be the expected
    assert response.status_code == 200
    answer = response.json()
    assert answer["method"] == "GET"
    assert answer["message"] == expected_msg
    assert answer["full_path"] == path


def test_any_other_post() -> None:
    # Given the hello path
    path = "qq"

    # And the expected response
    expected_msg = "Undefined request"

    # When call the app
    response = client.post(f"/{path}")

    # Then response must be the expected
    assert response.status_code == 200
    answer = response.json()
    assert answer["method"] == "POST"
    assert answer["message"] == expected_msg
    assert answer["full_path"] == path


def test_format_scheduling_1_open() -> None:
    # Given the base path
    path = "/format_scheduling"

    # And the body
    scheduling = {
        "monday": [
            {
                "type": "open",
                "value": 9 * 3600
            },
            {
                "type": "close",
                "value": 20 * 3600
            }
        ],
    }

    # And the expected response
    expected = format_from_formatted_days({WeekDays.monday: "9 AM - 8 PM"}).strip()

    # When format the scheduling
    response = client.post(path, json=scheduling)

    # Then response must be the expected
    assert response.status_code == 200
    assert response.text.strip() == expected


def test_format_scheduling_2_open() -> None:
    # Given the base path
    path = "/format_scheduling"

    # And the body
    scheduling = {
        "monday": [
            {
                "type": "open",
                "value": 9 * 3600
            },
            {
                "type": "close",
                "value": 14 * 3600
            },
            {
                "type": "open",
                "value": 18 * 3600
            },
            {
                "type": "close",
                "value": 23 * 3600
            },
        ],
    }

    # And the expected response
    expected = format_from_formatted_days({WeekDays.monday: "9 AM - 2 PM, 6 PM - 11 PM"}).strip()

    # When format the scheduling
    response = client.post(path, json=scheduling)

    # Then response must be the expected
    assert response.status_code == 200
    assert response.text.strip() == expected


def test_format_scheduling_special_times() -> None:
    # Given the base path
    path = "/format_scheduling"

    # And the body
    scheduling = {
        "monday": [
            {
                "type": "open",
                "value": 9 * 3600 + 5 * 60
            },
            {
                "type": "close",
                "value": 20 * 3600 + 50
            }
        ],
    }

    # And the expected response
    expected = format_from_formatted_days({WeekDays.monday: "9:05 AM - 8:00:50 PM"}).strip()

    # When format the scheduling
    response = client.post(path, json=scheduling)

    # Then response must be the expected
    assert response.status_code == 200
    assert response.text.strip() == expected


def test_format_scheduling_close_next_day() -> None:
    # Given the base path
    path = "/format_scheduling"

    # And the body
    scheduling = {
        "friday": [
            {"type": "open", "value": 64800}
        ],
        "saturday": [
            {"type": "close", "value": 3600},
            {"type": "open", "value": 32400},
            {"type": "close", "value": 39600},
            {"type": "open", "value": 57600},
            {"type": "close", "value": 82800}
        ]
    }

    # And the expected response
    expected = clean("""
    Monday: Closed
    Tuesday: Closed
    Wednesday: Closed
    Thursday: Closed
    Friday: 6 PM - 1 AM
    Saturday: 9 AM - 11 AM, 4 PM - 11 PM
    Sunday: Closed
    """)

    # When format the scheduling
    response = client.post(path, json=scheduling)

    # Then response must be the expected
    assert response.status_code == 200
    assert response.text.strip() == expected


def test_format_scheduling_full_example() -> None:
    # Given the base path
    path = "/format_scheduling"

    # And the body
    scheduling = {
        "monday": [],
        "tuesday": [
            {"type": "open", "value": 36000},
            {"type": "close", "value": 64800}
        ],
        "wednesday": [],
        "thursday": [
            {"type": "open", "value": 37800},
            {"type": "close", "value": 64800}
        ],
        "friday": [
            {"type": "open", "value": 36000}
        ],
        "saturday": [
            {"type": "close", "value": 3600},
            {"type": "open", "value": 36000}
        ],
        "sunday": [
            {"type": "close", "value": 3600},
            {"type": "open", "value": 43200},
            {"type": "close", "value": 75600}
        ]
    }

    # And the expected response
    expected = clean("""
        Monday: Closed
        Tuesday: 10 AM - 6 PM
        Wednesday: Closed
        Thursday: 10:30 AM - 6 PM
        Friday: 10 AM - 1 AM
        Saturday: 10 AM - 1 AM
        Sunday: 12 PM - 9 PM
    """)

    # When format the scheduling
    response = client.post(path, json=scheduling)

    # Then response must be the expected
    assert response.status_code == 200
    assert response.text.strip() == expected
