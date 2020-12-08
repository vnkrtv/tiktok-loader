import math
import random
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
        soup = BeautifulSoup(page, 'lxml')
        for td in soup.find_all('td', attrs={'class': 'name'}):
            buf = td.find('a').text.split('[')
            tiktokers.append({
                'fullname': buf[0].strip(),
                'nickname': buf[1][:-1]
            })
    return tiktokers[:count]


class TikTikLoader:
    api: TikTokApi
    db: TikTokStorage
    proxies: list
    timeout: float

    def __init__(self, db: TikTokStorage, proxies: list, timeout: float):
        self.db = db
        self.api = TikTokApi.get_instance()
        self.proxies = proxies
        self.timeout = timeout

    def __get_proxy(self) -> str:
        return random.choice(self.proxies)

    def __get_tiktoker(self, user_dict: dict) -> dict:
        user_info = user_dict['userInfo']
        tiktoker = {
            'tiktocker_id': user_info['user']['id'],
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
            'authorName': music_dict['id'],
            'title': music_dict['id'],
            'playUrl': music_dict['id'],
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

            })
            audios.append(music)
            videos.append(video)
        return tiktoks, audios, videos

    def get_user(self, username: str) -> dict:
        user_dict = self.api.getUser(username=username,
                                     custom_verifyFp='',
                                     proxy=self.__get_proxy())
        user_tiktoks = user_dict['items']
        user_info = user_dict['userInfo']
