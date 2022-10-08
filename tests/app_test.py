from fastapi.testclient import TestClient
from app import app
import json

client = TestClient(app)


def test_hello():
    # Given the hello path
    path = "hello"

    # And the expected response
    expected = {"message": "Hello World"}

    # When call the app
    response = client.get(path)

    # Then response must be the expected
    assert response.status_code == 200
    assert response.json() == expected


def test_hello_path_parameter():
    # Given the base path
    base_path = "/hello"

    # And the parameter
    parameter = "Juan"

    # And the expected response
    expected = {"message": "Hello Juan0"}

    # When create the path and
    path = f"{base_path}/{parameter}"
    response = client.get(path)

    # Then response must be the expected
    assert response.status_code == 200
    assert response.json() == expected


def test_hello_query_parameter():
    # Given the base path
    base_path = "/hello"

    # And the parameter
    parameter = "Juan"
    optional_parameter = 1

    # And the expected response
    expected = {"message": "Hello Juan1"}

    # When create the path and
    path = f"{base_path}/{parameter}?number={optional_parameter}"
    response = client.get(path)

    # Then response must be the expected
    assert response.status_code == 200
    assert response.json() == expected


def test_format_scheduling():
    # Given the base path
    base_path = "/format_scheduling"

    # And the body
    scheduling = {
        "monday": [
            {
                "type": "open",
                "value": 32400
            },
            {
                "type": "close",
                "value": 72000
            }
        ],
    }

    # And the expected response
    expected = """
    A restaurant is open:
    Monday: 9 AM - 8 PM
    """.strip()

    # When format the scheduling
    response = client.post("/format_scheduling",)

    # Then response must be the expected
    print(f"response: {response.text}")
    assert response.status_code == 200
    assert response.text.strip() == expected
