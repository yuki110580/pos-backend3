from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os

from crud import get_product, create_transaction  # Supabase用に書き直してある想定
from supabase_client import supabase  # Supabase接続クライアントをインポート

app = FastAPI()

# CORS設定（本番環境URLは必要に応じて追加）
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://pos-frontend3-kmt0r1him-yukis-projects-c495b036.vercel.app"
    "https://pos-frontend3.vercel.app"  # ← 本番URL
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

    result = create_transaction(req.emp_cd, req.items)
    return result
