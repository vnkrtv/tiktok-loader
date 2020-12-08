import os
import time
import random

from src.postgres import TikTokStorage
from src.loader import TikTikLoader, get_top_tiktokers
from src.proxy import PROXIES

PG_HOST = os.getenv('PG_HOST', 'postgres')
PG_PORT = os.getenv('PG_PORT', 5432)
PG_NAME = os.getenv('PG_NAME', 'tiktok')
PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASS = os.getenv('PG_PASS', 'password')
TIMEOUT = os.getenv('TIMEOUT', 1)
TIKTOKERS_COUNT = os.getenv('TIKTOKERS_COUNT', 1000)


def main():
    db = TikTokStorage.connect(host=PG_HOST,
                               port=PG_PORT,
                               dbname=PG_NAME,
                               user=PG_USER,
                               password=PG_PASS)
    db.create_schema()

    top_tiktokers = get_top_tiktokers(count=TIKTOKERS_COUNT)
    nicknames = [tiktoker['nickname'] for tiktoker in top_tiktokers]

    loader = TikTikLoader(db=db,
                          proxies=PROXIES,
                          timeout=TIMEOUT)
    while True:
        for nickname in nicknames:
            loader.load_user(nickname)
            time.sleep(TIMEOUT + random.random())


if __name__ == '__main__':
    main()
