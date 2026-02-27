from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_login_fail():
    response = client.post("/token", data={"username": "wrong", "password": "password"})
    assert response.status_code == 401