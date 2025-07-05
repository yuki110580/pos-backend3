from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime

import os

from crud import get_product, create_transaction  # Supabase用に書き直してある想定
from supabase_client import supabase  # Supabase接続クライアントをインポート

app = FastAPI()

# CORS設定（本番環境URLは必要に応じて追加）
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://pos-frontend3-kmt0r1him-yukis-projects-c495b036.vercel.app",
    "https://pos-frontend3-rho.vercel.app"  # ← 本番URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# 商品1件取得エンドポイント
# ===========================
@app.get("/item/{code}")
def read_item(code: int):
    item = get_product(code)
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# ===========================
# 購入リクエスト用モデル
# ===========================
class Item(BaseModel):
    prd_id: int
    code: str
    name: str
    price: int
    qty: int

class PurchaseRequest(BaseModel):
    emp_cd: str = ""
    items: List[Item]

# ===========================
# 購入処理
# ===========================
@app.post("/purchase")
def purchase(req: PurchaseRequest):
    if not req.items:
        raise HTTPException(status_code=422, detail="購入商品が1件もありません")

    # result = create_transaction(req.emp_cd, req.items)
    now = datetime.now()
    total_amount = sum(item.price * item.qty for item in req.items)
    total_ex_tax = int(total_amount / 1.1)

    print("=== 購入リクエスト受信 ===")
    print("合計金額:", total_amount)
    print("従業員コード:", req.emp_cd)

    transaction = supabase.table("transactions").insert({
        "datetime": now.isoformat(),
        "emp_cd": req.emp_cd,
        "store_cd": "001",
        "pos_no": "001",
        "total_amount": total_amount
    }).execute()

    print("=== トランザクション登録結果 ===")
    print(transaction)

    # エラーハンドリング追加
    if not transaction.data:
        raise HTTPException(status_code=500, detail="トランザクション登録に失敗")


    trd_id = transaction.data[0]["trd_id"]

    for item in req.items:
        detail_result = supabase.table("transaction_details").insert({
            "trd_id": trd_id,
            "prd_code": item.code,
            "prd_name": item.name,
            "prd_price": item.price,
            "qty": item.qty,
            "tax_cd": "A"
        }).execute()

        print("=== 明細登録結果 ===")
        print(detail_result)


    return {
        "success": True,
        "total": total_amount,
        "total_ex_tax": total_ex_tax
    }

def create_transaction(emp_cd, items):
    total = sum(item["price"] for item in items)
    total_ex_tax = int(total / 1.1)

    return {
        "success": True,
        "total": total,
        "total_ex_tax": total_ex_tax
    }
