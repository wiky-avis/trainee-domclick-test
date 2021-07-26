import telegram
import os
from dotenv import load_dotenv

load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot_client = telegram.Bot(token=TELEGRAM_TOKEN)


def send_message(message, chat_id, bot_client):
    return bot_client.send_message(chat_id=chat_id, text=message)
