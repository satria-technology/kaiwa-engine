from domain.conversation.model import Message
from service.conversation.service import ConversationServiceImp
from infrastructure.sqlite.conversation.chat_repository import SQLiteChatRepository
from domain.conversation.repository import ChatCompletionRepository
from application.dto.message_dto import MessageDTO

chat_repository = SQLiteChatRepository(db_path="path/to/your/database.db")
chat_completion_repository = None  # Implement this repository as needed

conversation_service = ConversationServiceImp(
    chat_repository=chat_repository,
    chat_completion_repository=chat_completion_repository,
)

def handle_message(message_dto: MessageDTO):
    # Convert DTO to domain model
    message = Message(
        sender=message_dto.sender,
        receiver=message_dto.receiver,
        message=message_dto.message,
        sent_at=message_dto.sent_at,
    )
    response = conversation_service.respond_to_message(message)
    # Convert domain model back to DTO
    response_dto = MessageDTO(
        sender=response.sender,
        receiver=response.receiver,
        message=response.message,
        sent_at=response.sent_at,
    )
    return response_dto
