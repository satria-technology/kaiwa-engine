import datetime
from typing import Optional
from pydantic import BaseModel


class Participant(BaseModel):
    id: Optional[str] = None
    external_id: str
    channel: str
    name: str


class Message(BaseModel):
    id: Optional[str] = None
    sender: Participant
    receiver: Participant
    message: str
    sent_at: datetime.datetime
