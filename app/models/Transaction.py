from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    sender_account_id = Column(Integer, ForeignKey("bank_accounts.id"))
    receiver_account_id = Column(Integer, ForeignKey("bank_accounts.id"))
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sender_account = relationship("BankAccount", foreign_keys=[sender_account_id], back_populates="sent_transactions")
    receiver_account = relationship("BankAccount", foreign_keys=[receiver_account_id], back_populates="received_transactions")