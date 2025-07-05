from fastapi.testclient import TestClient
from main import app  # main.pyにFastAPI appが定義されている前提

client = TestClient(app)

def test_get_item_by_code():
    response = client.get("/item/4901234567054")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ポールペン" 

def test_get_nonexistent_item_by_code():
    response = client.get("/item/9999999999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

