import logging
import asyncio
from redis_client.redis_client import RedisClient
from config import MainConfig
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.log(logging.INFO, 'Welcome on board!')


async def redis_add_update_loop():
    rediska = RedisClient(MainConfig.REDIS_HOST, MainConfig.REDIS_PORT)
    rediska.redis_connect()
    while True:
        rediska.redis_add_new_tg_update()
        await asyncio.sleep(1.0)

loop = asyncio.get_event_loop()
asyncio.ensure_future(redis_add_update_loop())
loop.run_forever()
