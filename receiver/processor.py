import logging

from receiver.receiver import Receiver
from comands import server_commands
from telegram_api import telegram_api
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def process_data(data: dict, tg: 'telegram_api'):
    receiver = Receiver()
    msg_from = data.get('message').get('from').get('first_name')
    msg_text = data.get('message').get('text')
    file_id = receiver.check_is_file(data)

    # just message
    if not file_id:
        receiver.if_command_check(data.get('message').get('chat').get('id'),
                                  data.get('message').get('text'))
        logging.log(logging.INFO, f'New message from: {msg_from} - {msg_text}')
    # just file
    else:
        logging.log(logging.INFO, f'Got file: {file_id}. From: {msg_from}')
        result = tg.get_file_path(file_id)

        if result['ok']:
            file_result = tg.save_file(result.get('result').get('file_path'))
            path = server_commands.save_file_to_server(result.get('result').get('file_path'), file_result)
            logging.log(logging.INFO, f'File saved! {path}')
            tg.send_message(data.get('message').get('chat').get('id'), f'File saved! {path}')
        else:
            logging.log(logging.ERROR, 'Something gone wrong')
            tg.send_message(data.get('message').get('chat').get('id'), 'Something gone wrong')