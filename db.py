from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 自分のMySQLパスワードに置き換えてください！
DB_URL = "mysql+pymysql://root:Pinya216%@localhost:3306/pos_db"

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
