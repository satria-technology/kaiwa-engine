from service.conversation.service import ConversationServiceImp

chat_repository = None
chat_completion_repository = None

conversation_service = ConversationServiceImp(
    chat_repository=chat_repository,
    chat_completion_repository=chat_completion_repository,
)
