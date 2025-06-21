from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_defects_endpoint():
    response = client.get("/defects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
