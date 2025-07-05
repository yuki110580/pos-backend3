from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_purchase_success():
    payload = {
        "emp_cd": "EMP001",
        "items": [
            {
                "prd_id": 1,
                "code": "4901234567054",
                "name": "ポールペン",
                "price": 120
            }
        ]
    }
    response = client.post("/purchase", json=payload)
    print("🟢 Response JSON:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "total_ex_tax" in data
    assert data["total"] == 120
    assert data["total_ex_tax"] == round(120 / 1.1)  # 税抜換算の検証


def test_create_purchase_with_invalid_product():
    payload = {
        "emp_cd": "EMP001",
        "items": [
            {
                "prd_id": 999,
                "code": "4900000000000",
                "name": "ダミー商品",
                "price": 100
            }
        ]
    }
    response = client.post("/purchase", json=payload)
    print("🔴 Response JSON (invalid product):", response.json())
    assert response.status_code in [400, 500]
    assert "error" in response.json() or "detail" in response.json()

def test_create_purchase_with_empty_items():
    payload = {
        "emp_cd": "EMP001",
        "items": []
    }
    response = client.post("/purchase", json=payload)
    print("🔴 Response JSON (empty items):", response.json())
    assert response.status_code == 422


