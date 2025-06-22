from pydantic import BaseModel
from datetime import datetime

class BankAccountBase(BaseModel):
    account_number: str

class BankAccountCreate(BankAccountBase):
    pass

class BankAccount(BankAccountBase):
    id: int
    balance: float
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True