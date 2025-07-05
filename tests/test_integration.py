from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_item_by_valid_code():
    response = client.get("/item/4901234567054")
    print("🔍 Response JSON:", response.json()) 
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ポールペン"
    assert data["price"] == 120


from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_post_purchase_multiple_items():
    # 商品データ（DBに4901234567054, 4901234567047 が存在する前提）
    payload = {
        "emp_cd": "EMP001",
        "items": [
            {"prd_id": 1, "code": "4901234567054", "name": "ポールペン", "price": 120},
            {"prd_id": 2, "code": "4901234567047", "name": "ノート", "price": 150}
        ]
    }

    response = client.post("/purchase", json=payload)
    print("🛒 Multi-item purchase response:", response.json())

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["total"] == 270  # 120 + 150
