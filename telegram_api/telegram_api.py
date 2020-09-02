import requests


class TelegramApi:
    def __init__(self, token: str):
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

    def get_file_path(self, file_id) -> dict:
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}')
        return response.json()

    def save_file(self, file_path) -> bytes:
        response = requests.get(f'https://api.telegram.org/file/bot{self.token}/{file_path}')
        return response.content






