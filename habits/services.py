import requests
from django.conf import settings


class TelegramBot:
    URL = 'https://api.telegram.org/bot'
    TOKEN = settings.TELEGRAM_BOT_TOKEN

    def send_message(self, user_telegram_id, text):
        requests.post(
            url=f'{self.URL}{self.TOKEN}/sendMessage',
            data={
                'chat_id': user_telegram_id,
                'text': text
            }
        )
