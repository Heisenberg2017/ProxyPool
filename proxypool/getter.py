import asyncio

from itertools import chain

from proxypool.log import logger
from proxypool.db import RedisClient
from proxypool.crawler import get_proxies
from proxypool.settings import *
import sys


class Getter():
    def __init__(self):
        self.redis = RedisClient()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    
    def run(self):

        logger.debug('获取器开始执行')
        if not self.is_over_threshold():
            # 获取代理
            for proxy in chain.from_iterable(asyncio.run(get_proxies())):
                logger.info(f'Proxies is {proxy}')
                self.redis.add(proxy)
