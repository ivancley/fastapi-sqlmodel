from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class ContextCreate(BaseModel):
    name: str

class ContextRead(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ContextUpdate(BaseModel):
    name: Optional[str] = None