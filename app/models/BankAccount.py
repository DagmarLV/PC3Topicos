from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="accounts")
    sent_transactions = relationship("Transaction", foreign_keys="[Transaction.sender_account_id]", back_populates="sender_account")
    received_transactions = relationship("Transaction", foreign_keys="[Transaction.receiver_account_id]", back_populates="receiver_account")