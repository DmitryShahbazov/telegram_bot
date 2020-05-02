from telegram_api.telegram_api import TelegramApi
from config import MainConfig
from comands import vpn_commands
from enum import Enum

class ReceiverCommands(Enum):
    vpn_status_log = '/vpn_status_log'
    help_command = '/help'


class Receiver:
    def __init__(self):
        self.api = TelegramApi(MainConfig.TOKEN)

    def if_command_check(self, chat_id, message):
        if not message[0] == '/':
            self.api.send_message(chat_id, 'Command should start with /')
        if message not in ReceiverCommands.value:
            self.api.send_message(chat_id, 'Command not found. Check /help')
        else:
            self.what_command_check(message, chat_id)

    def what_command_check(self, command, chat_id):
        if command == ReceiverCommands.help_command:
            self.api.send_message(chat_id, 'Here would be help soon..')
        elif command == ReceiverCommands.vpn_status_log:
            self.api.send_message(chat_id, vpn_commands.read_vpn_status_log())
