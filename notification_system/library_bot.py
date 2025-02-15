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

from user.models import User

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


def send_overdue_message(
    user: User = None, books: str = None, overdue: bool = True
):
    name_for_msg = (
        user.get_full_name()
        if user.first_name or user.last_name
        else user.email
    )
    if overdue:
        message = (
            f"{name_for_msg},\n"
            f"Your borrowings:\n"
            f"{books}\n"
            f"are expired.\n"
            f"Please return it as soon as possible!"
        )
    else:
        message = "No borrowings overdue today!"

    payload["text"] = message
    return requests.post(URL, data=payload)


def send_returned_message(user, book, borrowing):
    name_for_msg = (
        user.get_full_name()
        if user.first_name or user.last_name
        else user.email
    )
    message = (
        f"{name_for_msg} has returned "
        f"{book.title} on "
        f"{borrowing.actual_return_date}"
    )

    payload["text"] = message
    return requests.post(URL, data=payload)


def send_created_message(user, book, date):
    name_for_msg = (
        user.get_full_name()
        if user.first_name or user.last_name
        else user.email
    )
    message = f"{name_for_msg} has borrowed {book.title} until {date}"

    payload["text"] = message

    return requests.post(URL, data=payload)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"I'm a Library bot, I'll notify you about borrowings "
        f"in our chat! You can access the chat here: {CHAT_LINK}",
    )


def main() -> None:

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
