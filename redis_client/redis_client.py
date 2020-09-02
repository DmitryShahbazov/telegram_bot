import redis
import logging
from config import MainConfig
from telegram_api.telegram_api import TelegramApi
from receiver.receiver import Receiver
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class RedisClient:
    def __init__(self, host: str, port: int):
        self.redis_client = None
        self.host = host
        self.port = port

    def redis_connect(self):
        self.redis_client = redis.Redis(self.host, self.port)

    def redis_add_new_tg_update(self):
        tg = TelegramApi(MainConfig.TOKEN)
        update_data = tg.get_updates()

        if not update_data['result']:
            logging.log(logging.CRITICAL, 'Redis update data failed..')
            return

        for data in update_data['result']:
            if_update_exists = self.redis_client.get(data['update_id'])
            if not if_update_exists:
                receiver = Receiver()
                msg_from = data.get('message').get('from').get('first_name')
                msg_text = data.get('message').get('text')
                file_id = receiver.check_is_file(data)
                if not file_id:
                    receiver.if_command_check(data.get('message').get('chat').get('id'),
                                              data.get('message').get('text'))
                else:
                    logging.log(logging.INFO, f'Got file: {file_id}')
                    result = tg.get_file_path(file_id)
                    if result['ok']:
                        print(result)
                        file_result = tg.save_file(result.get('result').get('file_path'))
                        print(file_result)
                    logging.log(logging.INFO, f'FILE TO SAVE: {result}')
                logging.log(logging.INFO, f'New message from: {msg_from} - {msg_text}')
            self.redis_client.set(data['update_id'], str(data), nx=True)
