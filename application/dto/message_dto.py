from pydantic import BaseModel
from datetime import datetime


class MessageDTO(BaseModel):
    sender: str
    receiver: str
    message: str
    sent_at: datetime
