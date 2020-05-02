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


async def rediska_check():
    rediska = RedisClient(MainConfig.REDIS_HOST, MainConfig.REDIS_PORT)
    rediska.redis_connect()
    while True:
        x = rediska.redis_add_new_tg_update()
        print(x)
        await asyncio.sleep(0.1)


async def printing():
    while True:
        print('-----------------salam--------------------')
        await asyncio.sleep(0.5)


loop = asyncio.get_event_loop()
asyncio.ensure_future(rediska_check())
asyncio.ensure_future(printing())
loop.run_forever()
