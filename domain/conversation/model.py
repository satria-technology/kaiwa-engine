import datetime
from pydantic import BaseModel


class Participant(BaseModel):
    id: str
    phone_number: str
    channel: str
    name: str


class Message(BaseModel):
    id: str
    sender: Participant
    receiver: Participant
    message: str
    sent_at: datetime.datetime
