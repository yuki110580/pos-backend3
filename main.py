from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import SessionLocal
from crud import get_product
import os

app = FastAPI()

# 開発環境と本番環境の両方に対応するCORS設定
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # 本番環境のURLを追加する場合はここに追加
]

# CORSの設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/item/{code}")
def read_item(code: int):
    db = SessionLocal()
    try:
        item = get_product(db, code)
        if item:
            return {
                "prd_id": item.PRD_ID,
                "code": item.CODE,
                "name": item.NAME,
                "price": item.PRICE
            }
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    finally:
        db.close()

from pydantic import BaseModel
from typing import List
from crud import create_transaction

class Item(BaseModel):
    prd_id: int
    code: str
    name: str
    price: int

class PurchaseRequest(BaseModel):
    emp_cd: str = ""
    items: List[Item]

@app.post("/purchase")
def purchase(req: PurchaseRequest):
    if not req.items:
        raise HTTPException(status_code=422, detail="購入商品が1件もありません")

    db = SessionLocal()
    try:
        result = create_transaction(db, req.emp_cd, [item.dict() for item in req.items])
        return result
    finally:
        db.close()

# 一時的に main.py に以下を追加しておくと自動作成されます（最初の1回だけ）
from models import Base, Product, Transaction, TransactionDetail
from db import engine
# Base.metadata.create_all(bind=engine)  # 一時的にコメントアウト
