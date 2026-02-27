from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "docs": "/docs", "message": "API lista para CI/CD"}

def test_create_item_no_auth():
    response = client.post("/api/items", json={"name": "Test", "status": "Pendiente"})
    assert response.status_code == 401