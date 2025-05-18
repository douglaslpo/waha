from pydantic import BaseModel
from typing import Optional

class MessageRequest(BaseModel):
    number: str
    message: str

class MessageResponse(BaseModel):
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None 