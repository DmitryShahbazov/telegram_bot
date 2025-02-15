import redis
import logging
from config import MainConfig
from telegram_api.telegram_api import TelegramApi
from receiver.processor import process_data
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
                process_data(data, tg)

            self.redis_client.set(data['update_id'], str(data), nx=True)
