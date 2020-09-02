from typing import Optional

from telegram_api.telegram_api import TelegramApi
from config import MainConfig
from comands import server_commands
from enum import Enum


class ReceiverCommands(Enum):
    vpn_status_log = '/vpn_status_log'
    create_vpn_profile = '/create_vpn_profile'
    help_command = '/help'
    server_debug = '/server_debug'
    save_file = '/save_file'


class Receiver:
    def __init__(self):
        self.api = TelegramApi(MainConfig.TOKEN)

    @staticmethod
    def check_is_file(data: dict) -> Optional[str]:
        print(data)
        for key, v in data.items():
            if isinstance(v, dict):
                for k, val in v.items():
                    # audio, video
                    if isinstance(val, dict) and val.get('file_id'):
                        return val.get('file_id')
                    # photo; -1 = best quality
                    elif isinstance(val, list):
                        return val[-1].get('file_id')

    @staticmethod
    def split_message(message: str):
        # Проверяем не пришла ли команда с текстом
        splited_command = message.split(' ')
        if len(splited_command) > 1:
            return splited_command[0], splited_command[1]
        else:
            return message

    def if_command_check(self, chat_id: int, message: str):
        """
        Проверяем прислали ли нам команду
        1. Команда должна начинаться с /
        2. Команда должна быть добавлена в enum ReceiverCommands
        :param chat_id: Откуда пришло сообщение
        :param message: Содержание сообщения
        """
        if message:
            message, text = self.split_message(message)
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
        message, text = self.split_message(command)

        if command == ReceiverCommands.help_command.value:
            self.api.send_message(chat_id, f'List of current commands:{list(map(lambda c: c.value, ReceiverCommands))}')
        elif command == ReceiverCommands.vpn_status_log.value:
            self.api.send_message(chat_id, server_commands.read_vpn_status_log())
        elif command == ReceiverCommands.server_debug.value:
            MainConfig.SERVER_DEBUG = not MainConfig.SERVER_DEBUG
            self.api.send_message(chat_id, f'Server debug mode is {MainConfig.SERVER_DEBUG}')
        elif command == ReceiverCommands.create_vpn_profile.value:
            server_commands.create_vpn_profile(text)
