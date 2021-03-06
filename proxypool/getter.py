import asyncio

from aiohttp import ClientSession

from proxypool.log import logger
from proxypool.db import RedisClient
from proxypool.crawler import IPCrawlerBase
from proxypool.pipelines import ITEM_PIPELINES
from proxypool.settings import *


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

    @staticmethod
    def process_item(item):
        for pipeline_info in sorted(ITEM_PIPELINES.items(), key=lambda item: item[1]):
            pipeline_func, weight = pipeline_info
            item = pipeline_func(item)

    async def task_wrapper(self, cor):
        async for proxies_gen in cor:
            for proxies in proxies_gen:
                Getter.process_item(proxies)

    async def get_proxies(self):
        tasks = []
        async with ClientSession() as session:
            for sub in IPCrawlerBase.__subclasses__():
                cor = sub().get_proxies(session=session)
                tasks.append(self.task_wrapper(cor))
            await asyncio.gather(*tasks)

    def run(self):

        logger.debug('获取器开始执行')
        if not self.is_over_threshold():
            asyncio.run(self.get_proxies())
