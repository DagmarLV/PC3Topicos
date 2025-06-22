from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    receiver_account_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    sender_account_id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Deposit(BaseModel):
    amount: float
    receiver_account_id: int

class Withdraw(BaseModel):
    amount: float
    sender_account_id: int