import json
import redis
import logging
from config import MainConfig
from telegram_api.telegram_api import TelegramApi
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
        update_data = tg.api_get_updates()
        for data in update_data['result']:
            if_update_exists = self.redis_client.get(data['update_id'])
            if not if_update_exists:
                msg_from = data.get('message').get('from').get('first_name')
                msg_text = data.get('message').get('text')
                logging.log(logging.INFO, f'New message from: {msg_from} - {msg_text}')
            self.redis_client.set(data['update_id'], str(data), nx=True)
