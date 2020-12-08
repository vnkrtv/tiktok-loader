from typing import Generator

import psycopg2


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

    def add_tiktoker(self, tiktoker: dict):
        sql = '''
            INSERT INTO 
                tiktockers (tiktocker_id, sec_uid, unique_id, nickname, create_time, followers_count, following_count) 
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (tiktocker_id)
                DO UPDATE SET
                    followers_count = EXCLUDED.followers_count,
                    following_count = EXCLUDED.following_count'''
        params = [
            tiktoker['tiktocker_id'],
            tiktoker['sec_uid'],
            tiktoker['unique_id'],
            tiktoker['nickname'],
            tiktoker['create_time'],
            tiktoker['followers_count'],
            tiktoker['following_count']]
        self.exec(sql=sql, params=params)

    def add_tiktok(self, tiktok: dict):
        sql = '''
            INSERT INTO 
                tiktocks (tiktok_id, create_time, description, author_id, video_id, music_id, 
                          digg_count, share_count, comment_count, play_count, is_ad) 
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (tiktocker_id)
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

    def get_posts(self,
                  count: int = 0,
                  habs_list: list = None,
                  tags_list: list = None) -> Generator:
        if not habs_list and not tags_list:
            cursor = self.conn.cursor()
            sql = 'SELECT * FROM posts'
            if count:
                sql += ' LIMIT %d' % count
            cursor.execute(sql)
            return (post for post in cursor.fetchall())
        elif habs_list:
            return self.__get_posts_by_habs(count, habs_list)
        elif tags_list:
            return self.__get_posts_by_tags(count, tags_list)

    def get_posts_texts(self,
                        count: int = 0,
                        habs_list: list = None,
                        tags_list: list = None) -> Generator:
        posts_texts_gen = (post[2] for post in self.get_posts(count, habs_list, tags_list))
        return posts_texts_gen

    def __get_posts_by_habs(self,
                            count: int,
                            habs_list: list) -> Generator:
        sql = '''SELECT P.* 
                   FROM posts P JOIN habs H ON P.post_id = H.post_id
                  WHERE H.hab in (%s)''' % ''.join(["'" + str(hab) + "', " for hab in habs_list])[:-2]
        sql = sql + " LIMIT %d" % count if count > 0 else sql
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return (post for post in cursor.fetchall())

    def __get_posts_by_tags(self,
                            count: int,
                            tags_list: list) -> Generator:
        sql = '''SELECT P.* 
                   FROM posts P JOIN tags T ON P.post_id = T.post_id
                  WHERE T.tag in (%s)''' % ''.join(["'" + str(tag) + "', " for tag in tags_list])[:-2]
        sql = sql + " LIMIT %d" % count if count > 0 else sql
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return (post for post in cursor.fetchall())