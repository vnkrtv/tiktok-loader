import math
import random
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from TikTokApi import TikTokApi

from .postgres import TikTokStorage


def get_top_tiktokers(count: int = 1000) -> list:
    users_on_page = 100
    href = 'https://www.t30p.ru/TikTok.aspx?p={}&order=0'
    pages_count = math.ceil(count / users_on_page)
    tiktokers = []
    for p in range(1, pages_count + 1):
        page = requests.get(href.format(p)).content
        soup = BeautifulSoup(page, 'html.parser')
        for td in soup.find_all('td', attrs={'class': 'name'}):
            buf = td.find('a').text.split('[')
            tiktokers.append({
                'fullname': buf[0].strip(),
                'nickname': buf[1][:-1]
            })
    return tiktokers[:count]


class TikTokLoader:
    api: TikTokApi
    db: TikTokStorage
    proxies: list
    timeout: float

    def __init__(self, db: TikTokStorage, proxies: list, timeout: float):
        self.db = db
        self.api = TikTokApi.get_instance()
        self.proxies = proxies
        self.timeout = timeout

        self.proxies_indexes = set(range(len(proxies)))

    def __get_proxy(self) -> str:
        if len(self.proxies_indexes) == 0:
            self.proxies_indexes = set(range(len(self.proxies)))

        index = random.choice(self.proxies_indexes)
        self.proxies_indexes.remove(index)
        return self.proxies[index]

    def __get_tiktoker(self, user_dict: dict) -> dict:
        user_info = user_dict['userInfo']
        tiktoker = {
            'tiktoker_id': user_info['user']['id'],
            'sec_uid': user_info['user']['secUid'],
            'unique_id': user_info['user']['uniqueId'],
            'nickname': user_info['user']['nickname'],
            'create_time': datetime.fromtimestamp(user_info['user']['createTime']),
            'followers_count': user_info['stats']['followerCount'],
            'following_count': user_info['stats']['followingCount'],
            'heart': user_info['stats']['heart'],
            'heart_count': user_info['stats']['heartCount'],
            'video_count': user_info['stats']['videoCount'],
            'digg_count': user_info['stats']['diggCount']
        }
        return tiktoker

    def __get_music(self, tiktic_dict: dict) -> dict:
        music_dict = tiktic_dict['music']
        music = {
            'music_id': music_dict['id'],
            'author_name': music_dict['authorName'],
            'title': music_dict['title'],
            'play_url': music_dict['playUrl'],
            'duration': music_dict['id'],
            'album': music_dict['id']
        }
        return music

    def __get_video(self, tiktic_dict: dict) -> dict:
        video_dict = tiktic_dict['video']
        video = {
            'video_id': video_dict['id'],
            'height': video_dict['height'],
            'width': video_dict['width'],
            'ratio': video_dict['ratio'],
            'cover': video_dict['cover'],
            'play_url': video_dict['playUrl'],
            'duration': video_dict['duration'],
        }
        return video

    def __get_tiktoks(self, user_dict: dict) -> tuple:
        tiktoks = []
        audios = []
        videos = []
        for tiktok in user_dict['items']:
            music = self.__get_music(tiktok)
            video = self.__get_video(tiktok)
            tiktoks.append({
                'tiktok_id': tiktok['id'],
                'create_time': datetime.fromtimestamp(tiktok['createTime']),
                'description': tiktok['desc'],
                'author_id': tiktok['author']['id'],
                'is_ad': tiktok['isAd'],
                'video_id': video['id'],
                'music_id': music['id'],
                'digg_count': tiktok['stats']['diggCount'],
                'share_count': tiktok['stats']['shareCount'],
                'comment_count': tiktok['stats']['commentCount'],
                'play_count': tiktok['stats']['playCount']
            })
            audios.append(music)
            videos.append(video)
        return tiktoks, audios, videos

    def load_user(self, nickname: str):
        user_dict = self.api.getUser(username=nickname,
                                     custom_verifyFp='',
                                     proxy=self.__get_proxy())
        tiktoker = self.__get_tiktoker(user_dict)
        tiktoks, audios, videos = self.__get_tiktoks(user_dict)

        self.db.add_tiktoker(tiktoker)
        for tiktok in tiktoks:
            self.db.add_tiktok(tiktok)
        for music in audios:
            self.db.add_music(music)
        for video in videos:
            self.db.add_video(video)

    def load_users(self, nicknames_list: list):
        counter = 0
        for nickname in nicknames_list:
            self.load_user(nickname)
            counter += 1
            time.sleep(self.timeout + random.random())
            if counter % len(self.proxies) == 0:
                time.sleep(self.timeout * 600 + random.random())
