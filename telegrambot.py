from utils.logging import log
import os
from dotenv import load_dotenv
load_dotenv()

from telegram import Update
from telegram.ext import ApplicationBuilder
from interfaces.telegram.conversation import conversation_handler


app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

app.add_handler(conversation_handler)


log.info("Starting polling")

app.run_polling(
    allowed_updates=[Update.MESSAGE]
)
