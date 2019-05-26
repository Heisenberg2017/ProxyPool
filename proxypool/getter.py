import asyncio

from itertools import chain
from aiohttp import ClientSession

from proxypool.log import logger
from proxypool.db import RedisClient
from proxypool.crawler import IPCrawlerBase
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

    async def quote_persist(self, cor):
        async for parse_gen in cor:
            for proxies in parse_gen:
                self.redis.add(proxies)

    async def get_proxies(self):
        tasks = []
        async with ClientSession() as session:
            for sub in IPCrawlerBase.__subclasses__():
                cor = sub().get_proxies(session=session)
                tasks.append(self.quote_persist(cor))
            await asyncio.gather(*tasks)

    def run(self):

        logger.debug('获取器开始执行')
        if not self.is_over_threshold():
            asyncio.run(self.get_proxies())
