from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
from application.conversation import conversation_service
from domain.conversation.model import Message, Participant

__FREE_TEXT = range(1)

async def __start_handler(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="はじめましょう。")
    return __FREE_TEXT

def __parse_update_to_message(update: Update) -> Message:
    sender = Participant(
        external_id=str(update.message.from_user.id),  # Using user_id as a unique identifier
        channel="telegram",
        name=update.message.from_user.first_name
    )

    receiver = Participant(
        external_id=str(update.message.chat.id),  # Using chat_id as a unique identifier
        channel="telegram",
        name="kaiwa"
    )
    
    message = Message(
        sender=sender,
        receiver=receiver,
        message=update.message.text,
        sent_at=update.message.date
    )

    return message

async def __free_text_handler(update: Update, context: CallbackContext):
    message = __parse_update_to_message(update)
    response_message = conversation_service.respond_to_message(message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_message.message)
    return __FREE_TEXT

async def __cancel_handler(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="ありがとうございます。")
    return ConversationHandler.END

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("start", __start_handler)],
    states={
        __FREE_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, __free_text_handler)],
    },
    fallbacks=[CommandHandler("cancel", __cancel_handler)],
)
