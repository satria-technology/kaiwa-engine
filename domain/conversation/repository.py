from abc import ABC, abstractmethod

from domain.conversation.model import Message, Participant


class ChatCompletionRepository(ABC):
    @abstractmethod
    def text_generation(self, text: str) -> str:
        raise NotImplementedError


class ChatRepository(ABC):
    @abstractmethod
    def create_participant(self, participant: Participant):
        raise NotImplementedError
    
    def get_participant(self, participant: Participant):
        raise NotImplementedError
    
    @abstractmethod
    def save_outgoing_message(self, message: Message):
        raise NotImplementedError

    @abstractmethod
    def save_incoming_message(self, message: Message):
        raise NotImplementedError

    def retrieve_last_messages(self, limit: int) -> list[Message]:
        raise NotImplementedError
