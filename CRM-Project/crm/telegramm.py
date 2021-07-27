import logging
import logging.config

import telegram

from config import settings

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


bot_client = telegram.Bot(token=settings.TELEGRAM_TOKEN)


def send_message(message, chat_id, bot_client):
    return bot_client.send_message(chat_id=chat_id, text=message)
