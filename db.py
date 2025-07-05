from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

# SupabaseのPostgreSQL接続URLを使用
DB_URL = settings.DATABASE_URL

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
