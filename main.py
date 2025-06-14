from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import SessionLocal
from crud import get_product

app = FastAPI()

# CORSの設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
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
            return None
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
    db = SessionLocal()
    try:
        result = create_transaction(db, req.emp_cd, [item.dict() for item in req.items])
        return result
    finally:
        db.close()

# 一時的に main.py に以下を追加しておくと自動作成されます（最初の1回だけ）
from models import Base, Product, Transaction, TransactionDetail
from db import engine
Base.metadata.create_all(bind=engine)
