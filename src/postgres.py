from typing import Generator

import psycopg2

from .db_schema import DB_SCHEMA


class PostgresStorage:
    """
    Base class for working with PostgreSQL
    """

    conn: psycopg2.extensions.connection

    def __init__(self, conn):
        self.conn = conn

    @classmethod
    def connect(cls,
                host: str,
                port: int = 5432,
                user: str = 'postgres',
                password: str = 'password',
                dbname: str = 'postgres'):
        return cls(conn=psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=dbname)
        )

    def exec(self, sql: str, params: list) -> Generator:
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        return cursor.fetchall()


class TikTokStorage(PostgresStorage):
    """
    Class for working with TikTok
    """

    def create_schema(self):
        self.exec(sql=DB_SCHEMA, params=[])

    def add_tiktoker(self, tiktoker: dict):
        sql = '''
            INSERT INTO 
                tiktokers (tiktoker_id, sec_uid, unique_id, nickname, create_time, followers_count, 
                following_count, heart, heart_count, video_count, digg_count) 
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (tiktocker_id)
                DO UPDATE SET
                    followers_count = EXCLUDED.followers_count,
                    following_count = EXCLUDED.following_count,
                    heart=EXCLUDED.heart,
                    heartCount=EXCLUDED.heart_count,
                    videoCount=EXCLUDED.video_count,
                    diggCount=EXCLUDED.digg_count'''
        params = [
            tiktoker['tiktoker_id'],
            tiktoker['sec_uid'],
            tiktoker['unique_id'],
            tiktoker['nickname'],
            tiktoker['create_time'],
            tiktoker['followers_count'],
            tiktoker['following_count'],
            tiktoker['heart'],
            tiktoker['heart_count'],
            tiktoker['video_count'],
            tiktoker['digg_count']]
        self.exec(sql=sql, params=params)

    def add_music(self, music: dict):
        sql = '''
            INSERT INTO 
                music (music_id, author_name, title, play_url, duration, album) 
            VALUES 
                (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (music_id)
                DO NOTHING'''
        params = [
            music['music_id'],
            music['author_name'],
            music['title'],
            music['play_url'],
            music['duration'],
            music['album']]
        self.exec(sql=sql, params=params)

    def add_video(self, video: dict):
        sql = '''
            INSERT INTO 
                videos (video_id, height, width, ratio, cover, play_url, duration) 
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (video_id)
                DO NOTHING'''
        params = [
            video['video_id'],
            video['height'],
            video['width'],
            video['ratio'],
            video['cover'],
            video['play_url'],
            video['duration']]
        self.exec(sql=sql, params=params)

    def add_tiktok(self, tiktok: dict):
        sql = '''
            INSERT INTO 
                tiktoks (tiktok_id, create_time, description, author_id, video_id, music_id, 
                          digg_count, share_count, comment_count, play_count, is_ad) 
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (tiktok_id)
                DO UPDATE SET
                    digg_count = EXCLUDED.digg_count,
                    share_count = EXCLUDED.share_count,
                    comment_count = EXCLUDED.comment_count,
                    play_count = EXCLUDED.play_count'''
        params = [
            tiktok['tiktok_id'],
            tiktok['create_time'],
            tiktok['description'],
            tiktok['author_id'],
            tiktok['video_id'],
            tiktok['music_id'],
            tiktok['digg_count'],
            tiktok['share_count'],
            tiktok['comment_count'],
            tiktok['play_count'],
            tiktok['is_ad']]
        self.exec(sql=sql, params=params)

    def __get_all(self, table_name: str, count: int = 0) -> Generator:
        sql = f'SELECT * FROM {table_name}'
        if count != 0:
            sql += f' LIMIT {count}'
        return self.exec(sql=sql, params=[])

    def get_all_tiktokers(self, count: int = 0) -> Generator:
        return self.__get_all(table_name='tiktokers', count=count)

    def get_all_tiktoks(self, count: int = 0) -> Generator:
        return self.__get_all(table_name='tiktoks', count=count)

    def get_all_videos(self, count: int = 0) -> Generator:
        return self.__get_all(table_name='videos', count=count)

    def get_all_music(self, count: int = 0) -> Generator:
        return self.__get_all(table_name='music', count=count)

    def get_ticktoker(self, ticktoker_id: int = None, nickname: str = None) -> tuple:
        sql = f'SELECT * FROM tiktokers'
        if ticktoker_id:
            sql += f' WHERE tiktoker_id={ticktoker_id}'
        elif nickname:
            sql += f' WHERE nickname={nickname}'
        return next(self.exec(sql=sql, params=[]))

    def get_ticktoks(self, ticktok_id: int = None, author_id: int = None) -> Generator:
        sql = f'SELECT * FROM tiktoks'
        if ticktok_id:
            sql += f' WHERE tiktok_id={ticktok_id}'
        elif author_id:
            sql += f' WHERE author_id={author_id}'
        return self.exec(sql=sql, params=[])

    def get_music(self, music_id: int) -> tuple:
        sql = f'SELECT * FROM music WHERE music_id={music_id}'
        return next(self.exec(sql=sql, params=[]))

    def get_video(self, video_id: int) -> tuple:
        sql = f'SELECT * FROM videos WHERE video_id={video_id}'
        return next(self.exec(sql=sql, params=[]))
