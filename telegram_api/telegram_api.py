import requests


class TelegramApi:
    def __init__(self, token):
        self.token = token

    def get_me(self) -> dict:
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getMe')
        return response.json()

    def get_updates(self) -> dict:
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        return response.json()

    def send_message(self, chat_id, text) -> dict:
        response = requests.get(f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={text}')
        return response.json()






