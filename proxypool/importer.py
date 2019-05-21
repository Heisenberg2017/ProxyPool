from proxypool.db import RedisClient
from proxypool.log import logger

conn = RedisClient()


def set(proxy):
    result = conn.add(proxy)
    logger.debug(proxy)
    logger.debug('录入成功' if result else '录入失败')


def scan():
    logger.debug('请输入代理, 输入exit退出读入')
    while True:
        proxy = input()
        if proxy == 'exit':
            break
        set(proxy)


if __name__ == '__main__':
    scan()
