import datetime
from typing import Any, Optional
from fastapi import HTTPException, Request
from pydantic import BaseModel
import structlog

log = structlog.get_logger()

from domain.conversation.model import Message, Participant


class WhatsappWebhookPayload(BaseModel):
    ProfileName: Optional[str]
    From: str
    To: str
    Body: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.__message = None
        self.__normalize()

    def __normalize(self):
        sender = self.__parse_to_participant(self.From)
        sender.name = self.ProfileName if self.ProfileName is not None else "user"
        receiver = self.__parse_to_participant(self.To)

        self.__message = Message(
            sender=sender,
            receiver=receiver,
            message=self.Body,
            sent_at=datetime.datetime.now(),
        )

    def to_message(self) -> Message:
        if self.__message is None:
            raise ValueError("Call the object before accessing the message")
        return self.__message

    def __parse_to_participant(self, participant_str: str) -> Participant:
        try:
            channel, external_id = participant_str.split(":")
            return Participant(external_id=external_id, channel=channel, name="")
        except ValueError as e:
            log.error(
                "Invalid participant string",
                error=str(e),
                participant_str=participant_str,
                exc_info=True,
            )
            raise ValueError("Invalid participant string")
