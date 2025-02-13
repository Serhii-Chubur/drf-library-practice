import datetime
import logging
import os
import django
import requests

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application
from telegram.ext import ContextTypes, CommandHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service.settings")
django.setup()


load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)


BOT_TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHAT_LINK = os.getenv("CHAT_LINK")

payload = {"chat_id": CHAT_ID, "text": None}

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_overdue_message(user, books):
    message = (
        f"{user.get_full_name()} has borrowed:\n"
        f"{books}.\n"
        f"Your borrowings are expired.\n"
        f"Please return it as soon as possible!"
    )

    payload["text"] = message
    return requests.post(URL, data=payload)


def send_returned_message(user, book, borrowing):
    message = (
        f"{user.get_full_name()} has returned "
        f"{book.title} on "
        f"{borrowing.actual_return_date}"
    )

    payload["text"] = message
    return requests.post(URL, data=payload)


def send_created_message(user, book, date):
    message = (
        f"{user.get_full_name()} has borrowed "
        f"{book.title} until "
        f"{date}"
    )

    payload["text"] = message

    return requests.post(URL, data=payload)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"I'm a Library bot, I'll notify you about your borrowings "
        f"in our chat! You can access the chat here: {CHAT_LINK}",
    )


def main() -> None:

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
