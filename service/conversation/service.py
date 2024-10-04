import datetime
from domain.conversation import repository
from domain.conversation.model import Message
from domain.conversation.service import ConversationService

class ConversationServiceImp(ConversationService):
  def __init__(self, chat_repository: repository.ChatRepository, chat_completion_repository: repository.ChatCompletionRepository):
    self.chat_repository = chat_repository
    self.chat_completion_repository = chat_completion_repository
    
  def respond_to_message(self, message: Message) -> Message:
    self.chat_repository.save_incoming_message(message)
    response_message = Message(
      sender=message.receiver,
      receiver=message.sender,
    )
    try:
      response_message_body = self.chat_completion_repository.text_generation(message.message)
      response_message = Message(
        sender=message.receiver,
        receiver=message.sender,
        message=response_message_body,
        sent_at=datetime.datetime.now(),
      )
      self.chat_repository.save_outgoing_message(response_message)
    except Exception as e:
      print(e)
    finally:
      if response_message.message == "" or response_message.sent_at is None:
        response_message = Message(
          sender=message.receiver,
          receiver=message.sender,
          message="We are sorry, but we are unable to respond to your message at the moment.",
          sent_at=datetime.datetime.now(),
        )
      return response_message
