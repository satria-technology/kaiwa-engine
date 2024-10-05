import datetime
from domain.conversation import repository
from domain.conversation.model import Message
from domain.conversation.service import ConversationService


class ConversationServiceImp(ConversationService):
    def __init__(
        self,
        chat_repository: repository.ChatRepository,
        llm_repository: repository.LargeLanguageModelRepository,
    ):
        self.chat_repository = chat_repository
        self.llm_repository = llm_repository

    def respond_to_message(self, message: Message) -> Message:
        try:
            sender = self.chat_repository.get_participant(message.sender)
        except repository.ParticipantNotFoundError as e:
            sender = self.chat_repository.create_participant(message.sender)
        except Exception as e:
            raise e
        finally:
            if sender is not None: message.sender = sender

        try:
            receiver = self.chat_repository.get_participant(message.receiver)
        except repository.ParticipantNotFoundError as e:
            receiver = self.chat_repository.create_participant(message.receiver)
        except Exception as e:
            raise e
        finally:
            if receiver is not None: message.receiver = receiver

        try:
            context_messages = self.chat_repository.get_last_messages_to_participant(
                message.sender, 10, datetime.datetime.now() - datetime.timedelta(hours=1)
            )
            response_message = self.llm_repository.generate_text(context_messages)
            response_message.receiver = message.sender
            response_message.sender = message.receiver
            response_message.sent_at = datetime.datetime.now()
        except Exception as e:
            raise e
        
        self.__persist_message(message, response_message)
        return response_message

    async def __persist_message(self, incoming: Message, outcoming: Message):
        try:
            self.chat_repository.save_incoming_message(incoming)
            self.chat_repository.save_outgoing_message(outcoming)
        except Exception as e:
            print(e)
        return