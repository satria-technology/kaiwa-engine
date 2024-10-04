from abc import ABC, abstractmethod
from domain.conversation.model import Message


class ConversationService(ABC):
    @abstractmethod
    def respond_to_message(self, message: Message) -> Message:
        raise NotImplementedError
