import requests
from aiohttp import ClientSession
from requests.exceptions import ConnectionError

from proxypool.log import logger


base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    logger.info(f'正在抓取 {url}')
    resp = await session.request(method="GET", url=url, **kwargs)
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    resp.raise_for_status()
    logger.error(f'抓取成功 {url} {resp.status}')
    html = await resp.text()
    return html
