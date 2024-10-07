import datetime

import structlog
from domain.conversation import repository
from domain.conversation.model import Message
from domain.conversation.service import ConversationService
import threading

log = structlog.get_logger()


class ConversationServiceImp(ConversationService):
    __MAXIMUM_USER = 50
    __MAXIMUM_CONTEXT_MINUTES = 30
    __MAXIMUM_CONTEXT_COUNT = 20
    
    def __init__(
        self,
        chat_repository: repository.ChatRepository,
        llm_repository: repository.LargeLanguageModelRepository,
    ):
        self.chat_repository = chat_repository
        self.llm_repository = llm_repository
        self.locks = {}

    def respond_to_message(self, message: Message) -> Message:
        sender_key = message.sender.external_id

        if sender_key not in self.locks:
            self.locks[sender_key] = threading.Lock()

        mutex = self.locks[sender_key]
        with mutex:
            return self.__respond_to_message(message)
    
    def __respond_to_message(self, message: Message) -> Message:
        try:
            sender = self.chat_repository.get_participant(message.sender)
        except repository.ParticipantNotFoundError as e:
            if self.chat_repository.get_number_of_participants() > self.__MAXIMUM_USER:
                raise Exception("Maximum user reached")
            sender = self.chat_repository.create_participant(message.sender)
        except Exception as e:
            log.error("Error getting sender", error=str(e), exc_info=True)
            raise e
        finally:
            if sender is not None:
                message.sender = sender

        try:
            receiver = self.chat_repository.get_participant(message.receiver)
        except repository.ParticipantNotFoundError as e:
            message.receiver.name = "kaiwa"
            receiver = self.chat_repository.create_participant(message.receiver)
        except Exception as e:
            log.error("Error getting receiver", error=str(e), exc_info=True)
            raise e
        finally:
            if receiver is not None:
                message.receiver = receiver

        try:
            context_messages = self.chat_repository.get_last_messages_to_participant(
                message.sender,
                self.__MAXIMUM_CONTEXT_COUNT,
                datetime.datetime.now() - datetime.timedelta(minutes=self.__MAXIMUM_CONTEXT_MINUTES),
            )

            if len(context_messages) > 1 and context_messages[1].sent_at < datetime.datetime.now() - datetime.timedelta(
                seconds=30
            ):
                raise Exception("You are sending too many messages")


            context_messages = [message] + context_messages
            response_message_txt = self.llm_repository.generate_text(context_messages)
            response_message = Message(
                sender=message.sender,
                receiver=message.receiver,
                message=response_message_txt,
                sent_at=datetime.datetime.now(),
            )
        except Exception as e:
            log.error("Error generating response", error=str(e), exc_info=True)
            raise e

        self.__persist_message(message, response_message)
        return response_message

    async def __persist_message(self, incoming: Message, outcoming: Message):
        try:
            self.chat_repository.save_messages([incoming, outcoming])
        except Exception as e:
            log.error("Error saving messages", error=str(e), exc_info=True)
        return
