import json
import re
import asyncio
import abc

from collections.abc import Iterator

from aiohttp import ClientSession
from pyquery import PyQuery as pq

from proxypool.log import logger


class IPCrawlerBase(abc.ABC):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }

    @abc.abstractmethod
    def get_urls(self) -> Iterator:
        ''''''

    @abc.abstractmethod
    def parse(self, html: str) -> Iterator:
        ''''''

    @staticmethod
    async def fetch(url: str, session: ClientSession, **kwargs) -> str:
        logger.info(f'正在抓取 {url}')
        resp = await session.request(method="GET", url=url, **kwargs)
        logger.info("Got response [%s] for URL: %s", resp.status, url)
        resp.raise_for_status()
        logger.info(f'抓取成功 {url} {resp.status}')
        html = await resp.text()
        return html

    async def get_proxies(self, session: ClientSession) -> Iterator:
        ''''''

        for url in self.get_urls():
            html = None
            try:
                html = await self.fetch(url, session=session,
                                        headers=self.headers)
            except Exception as e:
                logger.warning(f'Crawl failed url {url} error {e}')
            else:
                logger.info(f'Crawl succeed {url}')
            if html is not None:
                yield self.parse(html)


class IP66Crawler(IPCrawlerBase):

    def get_urls(self) -> Iterator:
        page_count = 4
        start_url = 'http://www.66ip.cn/{}.html'
        return (start_url.format(page) for page in range(1, page_count + 1))

    def parse(self, html: str) -> Iterator:
        doc = pq(html)
        trs = doc('.containerbox table tr:gt(0)').items()
        for tr in trs:
            ip = tr.find('td:nth-child(1)').text()
            port = tr.find('td:nth-child(2)').text()
            yield ':'.join([ip, port])


class IP3366Crawler(IPCrawlerBase):

    def get_urls(self) -> Iterator:
        page_count = 4
        start_url = 'http://www.ip3366.net/free/?stype=1&page={}'
        return (start_url.format(page) for page in range(1, page_count + 1))

    def parse(self, html: str) -> Iterator:
        ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
        # \s * 匹配空格，起到换行作用
        re_ip_address = ip_address.findall(html)
        for address, port in re_ip_address:
            result = address + ':' + port
            yield result.replace(' ', '')


class KuaiDaiLiCrawler(IPCrawlerBase):

    def get_urls(self) -> Iterator:
        page_count = 4
        start_url = 'http://www.kuaidaili.com/free/inha/{}'
        return (start_url.format(page) for page in range(1, page_count + 1))

    def parse(self, html: str) -> Iterator:
        ip_address = re.compile('<td data-title="IP">(.*?)</td>')
        re_ip_address = ip_address.findall(html)
        port = re.compile('<td data-title="PORT">(.*?)</td>')
        re_port = port.findall(html)
        for address, port in zip(re_ip_address, re_port):
            address_port = address + ':' + port
            yield address_port.replace(' ', '')


class XiCiDaiLiCrawler(IPCrawlerBase):
    # headers = {
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
    #     'Host': 'www.xicidaili.com',
    #     'Referer': 'http://www.xicidaili.com/nn/3',
    #     'Upgrade-Insecure-Requests': '1',
    # }

    def get_urls(self) -> Iterator:
        page_count = 4
        start_url = 'http://www.xicidaili.com/nn/{}'
        return (start_url.format(page) for page in range(1, page_count + 1))

    def parse(self, html: str) -> Iterator:
        find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
        trs = find_trs.findall(html)
        for tr in trs:
            find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
            re_ip_address = find_ip.findall(tr)
            find_port = re.compile('<td>(\d+)</td>')
            re_port = find_port.findall(tr)
            for address, port in zip(re_ip_address, re_port):
                address_port = address + ':' + port
                yield address_port.replace(' ', '')


class IPHaiCrawler(IPCrawlerBase):

    def get_urls(self) -> Iterator:
        yield 'http://www.iphai.com/'

    def parse(self, html: str) -> Iterator:
        find_tr = re.compile('<tr>(.*?)</tr>', re.S)
        trs = find_tr.findall(html)
        for s in range(1, len(trs)):
            find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
            re_ip_address = find_ip.findall(trs[s])
            find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
            re_port = find_port.findall(trs[s])
            for address, port in zip(re_ip_address, re_port):
                address_port = address + ':' + port
                yield address_port.replace(' ', '')


class Data5UCrawler(IPCrawlerBase):

    # headers = {
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'Accept-Encoding': 'gzip, deflate',
    #     'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    #     'Cache-Control': 'max-age=0',
    #     'Connection': 'keep-alive',
    #     'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
    #     'Host': 'www.data5u.com',
    #     'Referer': 'http://www.data5u.com/free/index.shtml',
    #     'Upgrade-Insecure-Requests': '1',
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    # }

    def get_urls(self) -> Iterator:
        yield 'http://www.data5u.com/free/gngn/index.shtml'

    def parse(self, html: str) -> Iterator:
        ip_address = re.compile(
            '<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>',
            re.S)
        re_ip_address = ip_address.findall(html)
        for address, port in re_ip_address:
            result = address + ':' + port
            yield result.replace(' ', '')
