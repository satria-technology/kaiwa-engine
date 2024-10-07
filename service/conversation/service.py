import datetime
import pytz

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
            message.sender = self.chat_repository.get_participant_by_external_id(message.sender.external_id, message.sender.channel)
        except repository.ParticipantNotFoundError as e:
            if self.chat_repository.get_number_of_participants() > self.__MAXIMUM_USER:
                raise Exception("Maximum user reached")
            message.sender = self.chat_repository.create_participant(message.sender)
        except Exception as e:
            log.error("Error getting sender", error=str(e), exc_info=True)
            raise e

        try:
            message.receiver = self.chat_repository.get_participant_by_external_id(message.receiver.external_id, message.receiver.channel)
        except repository.ParticipantNotFoundError as e:
            message.receiver.name = "kaiwa"
            message.receiver = self.chat_repository.create_participant(message.receiver)
        except Exception as e:
            log.error("Error getting receiver", error=str(e), exc_info=True)
            raise e

        try:
            context_messages = self.chat_repository.get_last_messages_to_participant(
                message.sender,
                self.__MAXIMUM_CONTEXT_COUNT,
                datetime.datetime.now() - datetime.timedelta(minutes=self.__MAXIMUM_CONTEXT_MINUTES),
            )

            delta_time = datetime.datetime.now(pytz.utc) - datetime.timedelta(
                seconds=30
            )
            if len(context_messages) > 1 and context_messages[1].sent_at > delta_time:
                raise Exception("You are sending too many messages, wait for 30 seconds from your last message")


            context_messages = [message] + context_messages
            response_message_txt = self.llm_repository.generate_text(context_messages)
            response_message = Message(
                sender=message.receiver,
                receiver=message.sender,
                message=response_message_txt,
                sent_at=datetime.datetime.now(pytz.utc),
            )
        except Exception as e:
            log.error("Error generating response", error=str(e), exc_info=True)
            raise e

        self.__persist_message(message, response_message)
        return response_message

    def __persist_message(self, incoming: Message, outcoming: Message):
        try:
            self.chat_repository.save_messages([incoming, outcoming])
        except Exception as e:
            log.error("Error saving messages", error=str(e), exc_info=True)
        return
