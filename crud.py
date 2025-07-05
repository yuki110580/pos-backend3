# crud.py
from supabase_client import supabase

def get_product(code: int):
    response = supabase.table("products").select("*").eq("code", code).single().execute()
    if response.data:
        return response.data
    return None

def create_transaction(emp_cd: str, items: list):
    # 1. 取引の登録
    from datetime import datetime
    now = datetime.now().isoformat()

    transaction = {
        "emp_cd": emp_cd,
        "date": now,
    }
    trans_resp = supabase.table("transactions").insert(transaction).execute()
    transaction_id = trans_resp.data[0]["id"]

    # 2. 取引詳細の登録
    total = 0
    for item in items:
        supabase.table("transaction_details").insert({
            "transaction_id": transaction_id,
            "prd_id": item.prd_id,
            "code": item.code,
            "name": item.name,
            "price": item.price
        }).execute()
        total += item.price

    return {"message": "Transaction completed", "transaction_id": transaction_id, "total": total}


