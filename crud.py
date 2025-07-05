from models import Product, Transaction, TransactionDetail
from sqlalchemy.orm import Session  # ← これが必要
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

def get_product(db: Session, code: int):
    return db.query(Product).filter(Product.CODE == code).first()

def create_transaction(db: Session, emp_cd: str, items: list):
    try:
        # 1. 取引テーブルに登録（初期値で）
        emp_cd = emp_cd if emp_cd else "9999999999"
        new_trd = Transaction(EMP_CD=emp_cd)
        db.add(new_trd)
        db.commit()
        db.refresh(new_trd)
        trd_id = new_trd.TRD_ID

        # 2. 明細登録
        total = 0
        total_ex_tax = 0
        for i, item in enumerate(items):
            detail = TransactionDetail(
                TRD_ID=trd_id,
                DTL_ID=i + 1,
                PRD_ID=item["prd_id"],
                PRD_CODE=item["code"],
                PRD_NAME=item["name"],
                PRD_PRICE=item["price"],
            )
            db.add(detail)
            total += item["price"]
            total_ex_tax += round(item["price"] / 1.1)

        # 3. トータル更新
        db.query(Transaction).filter(Transaction.TRD_ID == trd_id).update({
            "TOTAL_AMT": total,
            "TTL_AMT_EX_TAX": total_ex_tax
        })
        db.commit()

        return {
            "success": True,
            "trd_id": trd_id,
            "total": total,
            "total_ex_tax": total_ex_tax
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="存在しない商品IDが含まれています")

