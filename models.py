from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "product_master"

    PRD_ID = Column(Integer, primary_key=True, index=True)
    CODE = Column(BigInteger, unique=True, index=True, nullable=False)
    NAME = Column(String(50), nullable=False)
    PRICE = Column(Integer, nullable=False)

# 既存のProduct定義の下に追加してください
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class Transaction(Base):
    __tablename__ = "transaction"

    TRD_ID = Column(Integer, primary_key=True, index=True)
    DATETIME = Column(DateTime, default=func.now())
    EMP_CD = Column(String(10), default="9999999999")
    STORE_CD = Column(String(5), default="30")
    POS_NO = Column(String(3), default="90")
    TOTAL_AMT = Column(Integer, default=0)
    TTL_AMT_EX_TAX = Column(Integer, default=0)

    details = relationship("TransactionDetail", back_populates="transaction")

class TransactionDetail(Base):
    __tablename__ = "transaction_detail"

    TRD_ID = Column(Integer, ForeignKey("transaction.TRD_ID"), primary_key=True)
    DTL_ID = Column(Integer, primary_key=True)
    PRD_ID = Column(Integer, ForeignKey("product_master.PRD_ID"))
    PRD_CODE = Column(String(13), nullable=False)
    PRD_NAME = Column(String(50), nullable=False)
    PRD_PRICE = Column(Integer, nullable=False)
    TAX_CD = Column(String(2), default="10")

    transaction = relationship("Transaction", back_populates="details")
