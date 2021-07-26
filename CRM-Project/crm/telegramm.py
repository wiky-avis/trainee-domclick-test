import telegram
import os
import logging
import logging.config
from dotenv import load_dotenv

load_dotenv()

LOGGING_CONFIG = {
    'version': 1,
    'handlers': {
        'fileHandler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'myFormatter',
            'filename': 'my_logger.log',
            'maxBytes': 50000000,
            'backupCount': 5,
            'encoding': 'utf-8'}},
    'loggers': {
        'info': {
            'handlers': ['fileHandler'],
            'level': 'INFO'},
        'debug': {
            'handlers': ['fileHandler'],
            'level': 'DEBUG'}},
    'formatters': {
        'myFormatter': {
            'format': '%(asctime)s, %(levelname)s, %(message)s'}}}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('info')
logger = logging.getLogger('debug')
logger.info('Настройка логгирования окончена!')


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot_client = telegram.Bot(token=TELEGRAM_TOKEN)


def send_message(message, chat_id, bot_client):
    return bot_client.send_message(chat_id=chat_id, text=message)
