import datetime
from typing import Optional
from pydantic import BaseModel


class Participant(BaseModel):
    id: Optional[int] = None
    external_id: str
    channel: str
    name: str


class Message(BaseModel):
    id: Optional[int] = None
    sender: Participant
    receiver: Participant
    message: str
    sent_at: datetime.datetime
