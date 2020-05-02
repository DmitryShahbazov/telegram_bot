import logging
import redis
import requests
import signal
import sys
import asyncio
from redis_client.redis_client import RedisClient
from config import MainConfig
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def read_vpn_status_log():
    with open('/etc/openvpn/server/openvpn-status.log', 'r') as log_file:
        log_text = log_file.read()
        log_file.close()
    return log_text


async def redis_add_update_loop():
    rediska = RedisClient(MainConfig.REDIS_HOST, MainConfig.REDIS_PORT)
    rediska.redis_connect()
    while True:
        data = rediska.redis_add_new_tg_update()
        print(data)
        for message in data:
            print(message)
            # msg_from = message.get('message').get('from').get('first_name')
            # msg_text = message.get('message').get('text')
            # logging.log(logging.INFO, f'New message from: {msg_from} - {msg_text}')
        await asyncio.sleep(0.1)

loop = asyncio.get_event_loop()
asyncio.ensure_future(redis_add_update_loop())
loop.run_forever()
