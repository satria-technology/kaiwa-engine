import datetime

import structlog
from domain.conversation import repository
from domain.conversation.model import Message
from domain.conversation.service import ConversationService

log = structlog.get_logger()
class ConversationServiceImp(ConversationService):
    def __init__(
        self,
        chat_repository: repository.ChatRepository,
        llm_repository: repository.LargeLanguageModelRepository,
    ):
        self.chat_repository = chat_repository
        self.llm_repository = llm_repository

    def respond_to_message(self, message: Message) -> Message:
        # TODO need to implement mutex with key message.sender
        
        try:
            sender = self.chat_repository.get_participant(message.sender)
        except repository.ParticipantNotFoundError as e:
            sender = self.chat_repository.create_participant(message.sender)
        except Exception as e:
            log.error("Error getting sender", error=str(e), exc_info=True)
            raise e
        finally:
            if sender is not None: message.sender = sender

        try:
            receiver = self.chat_repository.get_participant(message.receiver)
        except repository.ParticipantNotFoundError as e:
            message.receiver.name = "kaiwa"
            receiver = self.chat_repository.create_participant(message.receiver)
        except Exception as e:
            log.error("Error getting receiver", error=str(e), exc_info=True)
            raise e
        finally:
            if receiver is not None: message.receiver = receiver

        try:
            context_messages = self.chat_repository.get_last_messages_to_participant(
                message.sender, 10, datetime.datetime.now() - datetime.timedelta(hours=1)
            )

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