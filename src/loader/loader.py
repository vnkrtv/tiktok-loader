import math
import random

import requests
from bs4 import BeautifulSoup
from TikTokApi import TikTokApi


def get_top_tiktokers(count: int = 1000) -> list:
    users_on_page = 100
    href = 'https://www.t30p.ru/TikTok.aspx?p={}&order=0'
    pages_count = math.ceil(count / users_on_page)
    tiktokers = []
    for p in range(1, pages_count + 1):
        page = requests.get(href.format(p)).content
        soup = BeautifulSoup(page, 'lxml')
        for td in soup.find_all('td', attrs={'class': 'name'}):
            buf = td.find('a').text.split('[')
            tiktokers.append({
                'fullname': buf[0].strip(),
                'nickname': buf[1][:-1]
            })
    return tiktokers[:count]


class TikTikLoader:

    proxies: list
    timeout: float
    api: TikTokApi

    def __init__(self, proxies: list, timeout: float):
        self.api = TikTokApi.get_instance()
        self.proxies = proxies
        self.timeout = timeout

    def __get_proxy(self) -> str:
        return random.choice(self.proxies)

    def get_user(self, username: str) -> dict:
        self.api.


