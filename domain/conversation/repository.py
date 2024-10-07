from abc import ABC, abstractmethod
import datetime

from domain.conversation.model import Message, Participant


class ParticipantNotFoundError(Exception):
    def __init__(self):
        super().__init__(f"Participant not found")


class LargeLanguageModelRepository(ABC):
    @abstractmethod
    def generate_text(self, messages: list[Message]) -> str:
        raise NotImplementedError


class ChatRepository(ABC):
    @abstractmethod
    def create_participant(self, participant: Participant):
        raise NotImplementedError
    
    @abstractmethod
    def get_number_of_participants(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_participant(self, participant: Participant):
        raise NotImplementedError

    @abstractmethod
    def save_messages(self, messages: list[Message]):
        raise NotImplementedError

    @abstractmethod
    def get_last_messages_to_participant(
        self, participant: Participant, n: int, datetime: datetime.datetime
    ) -> list[Message]:
        raise NotImplementedError
