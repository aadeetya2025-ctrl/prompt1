import pytest
from main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200

def test_chat_vote(client):
    response = client.post("/chat", json={"message": "how to vote"})
    assert response.status_code == 200
    data = response.get_json()
    assert "reply" in data

def test_chat_register(client):
    response = client.post("/chat", json={"message": "register"})
    assert response.status_code == 200
    data = response.get_json()
    assert "reply" in data

def test_chat_no_message(client):
    response = client.post("/chat", json={})
    assert response.status_code == 400

def test_timeline(client):
    response = client.get("/timeline")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 5

def test_nearby_office(client):
    response = client.get("/nearbyoffice?city=Mumbai")
    assert response.status_code == 200
    data = response.get_json()
    assert "maps_url" in data
