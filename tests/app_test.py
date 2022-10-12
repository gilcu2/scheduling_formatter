from fastapi.testclient import TestClient
from app import app
import json
from scheduling_formatter.week_formatter import WeekDays, format_from_formatted_days
from scheduling_formatter.day_formatter import Action, ActionType

client = TestClient(app)


def test_any_get():
    # Given the hello path
    path = "qq"

    # And the expected response
    expected_msg = "Hello Wolt"

    # When call the app
    response = client.get(f"/{path}")

    # Then response must be the expected
    assert response.status_code == 200
    answer = response.json()
    assert answer["method"] == "GET"
    assert answer["message"] == expected_msg
    assert answer["full_path"] == path


def test_any_other_post():
    # Given the hello path
    path = "qq"

    # And the expected response
    expected_msg = "Hello Wolt"

    # When call the app
    response = client.post(f"/{path}")

    # Then response must be the expected
    assert response.status_code == 200
    answer = response.json()
    assert answer["method"] == "POST"
    assert answer["message"] == expected_msg
    assert answer["full_path"] == path


def test_format_scheduling_from_json():
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
    expected = """
    A restaurant is open:
    Monday: 9 AM - 8 PM
    """.strip()

    # When format the scheduling
    response = client.post(path, data=scheduling)

    # Then response must be the expected
    print(f"response: {response.text}")
    assert response.status_code == 200
    assert response.text.strip() == expected


def test_format_scheduling():
    # Given a scheduling
    scheduling = {
        WeekDays.monday: [
            Action(type=ActionType.open, value=9 * 3600),
            Action(type=ActionType.close, value=20 * 3600),
        ],
    }

    # And the format_scheduling  path
    path = "/format_scheduling"

    # And the expected result
    expected = format_from_formatted_days({WeekDays.monday: "9 AM - 8 PM"})

    # When call the api
    response = client.post(path, data=scheduling)

    # Then response must be the expected
    assert response.status_code == 200
    assert response.json() == expected
