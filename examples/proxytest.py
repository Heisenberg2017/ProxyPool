import requests
from proxypool.settings import TEST_URL
from proxypool.log import logger

proxy = '96.9.90.90:8080'

proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy,
}

logger.debug(TEST_URL)
response = requests.get(TEST_URL, proxies=proxies, verify=False)
if response.status_code == 200:
    logger.debug('Successfully')
    logger.debug(response.text)