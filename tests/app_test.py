from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_root():
    # Given a client of the app

    # When ask the root path
    response = client.get("/")

    # Then answer must be the expected
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
