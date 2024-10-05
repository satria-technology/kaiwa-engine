import datetime
from fastapi import HTTPException, Request
from pydantic import BaseModel

from domain.conversation.model import Message, Participant


class WhatsappWebhookPayload(BaseModel):
    MessageSid: str
    AccountSid: str
    From: str
    To: str
    Body: str

    def to_message(self):
        sender = parse_whatsapp_number(self.From)
        receiver = parse_whatsapp_number(self.To)

        message = Message(
            sender=sender,
            receiver=receiver,
            message=self.Body,
            sent_at=datetime.datetime.now(),
        )

        return message

def parse_whatsapp_number(whatsapp_number: str) -> Participant:
    if whatsapp_number.startswith("whatsapp:"):
        phone_number = whatsapp_number[len("whatsapp:"):]
        return Participant(
            phone_number=phone_number,
            channel="whatsapp",
            name=""  # You can set a default name or leave it empty
        )
    else:
        raise ValueError("Invalid WhatsApp number format")
