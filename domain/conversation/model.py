import datetime
from pydantic import BaseModel

class User(BaseModel):
  phone_number: str
  name: str

class Message(BaseModel):
  sender: User
  receiver: User
  message: str
  sent_at: datetime.datetime