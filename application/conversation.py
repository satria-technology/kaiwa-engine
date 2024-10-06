import os
from domain.conversation.model import Message
from infrastructure.openapi.conversation.llm_repository import (
    OpenAIPlatformLLMRepository,
)
from service.conversation.service import ConversationServiceImp
from infrastructure.sqlite.conversation.chat_repository import SQLiteChatRepository
from application.dto.message_dto import MessageDTO

chat_repository = SQLiteChatRepository(db_file=os.getenv("SQLITE_DB_FILE"))
llm_repository = OpenAIPlatformLLMRepository(
    api_key=os.getenv("OPENAI_API_KEY"), model=os.getenv("OPENAI_CONVERSATION_MODEL")
)

conversation_service = ConversationServiceImp(
    chat_repository=chat_repository,
    llm_repository=llm_repository,
)
