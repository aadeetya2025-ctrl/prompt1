import pytest
from main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200

def test_chat_vote_response(client):
    response = client.post("/chat", json={"message": "how to vote"})
    assert response.status_code == 200
    data = response.get_json()
    assert "reply" in data
    assert "polling booth" in data["reply"].lower()

def test_chat_register_response(client):
    response = client.post("/chat", json={"message": "how to register"})
    assert response.status_code == 200
    data = response.get_json()
    assert "reply" in data
    assert "voterportal.eci.gov.in" in data["reply"].lower()

def test_chat_evm_response(client):
    response = client.post("/chat", json={"message": "what is evm"})
    assert response.status_code == 200
    data = response.get_json()
    assert "reply" in data
    assert "electronic voting machine" in data["reply"].lower()

def test_chat_timeline_response(client):
    response = client.post("/chat", json={"message": "election timeline"})
    assert response.status_code == 200
    data = response.get_json()
    assert "reply" in data
    assert "announcement of dates" in data["reply"].lower()

def test_chat_empty_message_returns_400(client):
    response = client.post("/chat", json={"message": "   "})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    
    response2 = client.post("/chat", json={})
    assert response2.status_code == 400

def test_timeline_returns_list(client):
    response = client.get("/timeline")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_timeline_has_5_phases(client):
    response = client.get("/timeline")
    data = response.get_json()
    assert len(data) >= 5
    for phase in data:
        assert "phase" in phase
        assert "duration" in phase
        assert "description" in phase

def test_nearby_office_returns_maps_url(client):
    response = client.get("/nearbyoffice?city=Mumbai")
    assert response.status_code == 200
    data = response.get_json()
    assert "maps_url" in data
    assert "message" in data
    assert "Mumbai" in data["maps_url"]

def test_search_returns_google_url(client):
    response = client.get("/search?q=voting process")
    assert response.status_code == 200
    data = response.get_json()
    assert "search_url" in data
    assert "knowledge_url" in data
    assert "voting+process" in data["search_url"]

def test_translate_route_exists(client):
    response = client.post("/translate", json={"text": "hello"})
    # Since this relies on live Google Cloud Translation APIs, it might return 500 if credentials are missing
    # or 200 if it succeeds. We just check that the route exists (not a 404).
    assert response.status_code != 404

def test_health_route_returns_healthy(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("status") == "healthy"
    assert "timestamp" in data
