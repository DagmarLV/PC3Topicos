from pydantic import BaseModel
from datetime import datetime

class AccessLogBase(BaseModel):
    action: str
    ip_address: str
    user_agent: str

class AccessLog(AccessLogBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True