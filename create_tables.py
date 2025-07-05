#!/usr/bin/env python3
"""
Supabaseにテーブルを作成するスクリプト
"""

from sqlalchemy import text
from db import engine
from models import Base

def create_tables():
    """データベースにテーブルを作成"""
    try:
        # SQLAlchemyのBaseを使用してテーブルを作成
        Base.metadata.create_all(bind=engine)
        print("✅ テーブルが正常に作成されました")
        
        # サンプルデータの挿入
        with engine.connect() as conn:
            # サンプル商品データ
            sample_products = [
                (1234567890123, 'コーラ', 150),
                (1234567890124, 'お茶', 120),
                (1234567890125, 'チョコレート', 200),
                (1234567890126, 'ポテトチップス', 180),
                (1234567890127, 'ジュース', 130)
            ]
            
            for code, name, price in sample_products:
                try:
                    conn.execute(text("""
                        INSERT INTO product_master (CODE, NAME, PRICE) 
                        VALUES (:code, :name, :price)
                        ON CONFLICT (CODE) DO NOTHING
                    """), {"code": code, "name": name, "price": price})
                except Exception as e:
                    print(f"⚠️ 商品データ挿入エラー: {e}")
            
            conn.commit()
            print("✅ サンプルデータが挿入されました")
            
    except Exception as e:
        print(f"❌ テーブル作成エラー: {e}")
        raise

if __name__ == "__main__":
    print("Supabaseにテーブルを作成中...")
    create_tables()
    print("完了！") 