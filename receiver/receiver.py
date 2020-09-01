from typing import Optional

from telegram_api.telegram_api import TelegramApi
from config import MainConfig
from comands import server_commands
from enum import Enum


class ReceiverCommands(Enum):
    vpn_status_log = '/vpn_status_log'
    help_command = '/help'
    server_debug = '/server_debug'
    save_file = '/save_file'


class Receiver:
    def __init__(self):
        self.api = TelegramApi(MainConfig.TOKEN)

    @staticmethod
    def check_is_file(data: dict) -> Optional[str]:
        for key, v in data.items():
            if isinstance(v, dict) and v.get('file_id'):
                return v.get('file_id')

    def if_command_check(self, chat_id: int, message: str):
        """
        Проверяем прислали ли нам команду
        1. Команда должна начинаться с /
        2. Команда должна быть добавлена в enum ReceiverCommands
        :param chat_id: Откуда пришло сообщение
        :param message: Содержание сообщения
        """
        if not message[0] == '/':
            self.api.send_message(chat_id, 'Command should start with /')
        elif message not in [item.value for item in ReceiverCommands]:
            self.api.send_message(chat_id, 'Command not found. Check /help')
        else:
            self.what_command_check(message, chat_id)

    def what_command_check(self, command: str, chat_id: int):
        """
        Проверяем что за команду нам прислали
        :param command: Сама команда
        :param chat_id: Откуда пришло сообщение
        """
        if command == ReceiverCommands.help_command.value:
            self.api.send_message(chat_id, f'List of current commands:{list(map(lambda c: c.value, ReceiverCommands))}')
        elif command == ReceiverCommands.vpn_status_log.value:
            self.api.send_message(chat_id, server_commands.read_vpn_status_log())
        elif command == ReceiverCommands.server_debug.value:
            MainConfig.SERVER_DEBUG = not MainConfig.SERVER_DEBUG
            self.api.send_message(chat_id, f'Server debug mode is {MainConfig.SERVER_DEBUG}')
