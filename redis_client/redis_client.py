import redis
from config import MainConfig
from telegram_api.telegram_api import TelegramApi


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
            self.redis_client.set(data['update_id'], str(data), nx=True)


