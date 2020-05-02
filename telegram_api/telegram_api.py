import requests


class TelegramApi:
    def __init__(self, token):
        self.token = token

    def api_get_me(self) -> dict:
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getMe')
        return response.json()

    def api_get_updates(self) -> dict:
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        return response.json()





