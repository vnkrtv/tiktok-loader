DB_SCHEMA = '''
CREATE TABLE IF NOT EXISTS tiktockers
(
    tiktocker_id    text,
    sec_uid         text
        not null,
    unique_id       text
        unique
        not null,
    nickname        text
        not null,
    create_time     timestamp
        not null,
    followers_count int8,
    following_count int8,
    heart           int8,
    heart_count     int8,
    video_count     int8,
    digg_count      int8,

    constraint pk_users primary key (tiktocker_id)
);

CREATE TABLE IF NOT EXISTS music
(
    music_id    text,
    author_name text,
    title       text,
    play_url    text,
    duration    int4,
    album       text
);

CREATE TABLE IF NOT EXISTS videos
(
    video_id    text,
    height      int4,
    width       int4,
    ratio       text,
    cover       text,
    play_url    text,
    duration    int4,
);

CREATE TABLE IF NOT EXISTS tiktocks
(
    tiktok_id     text,
    create_time   timestamp
        not null,
    description   text,
    author_id     int8
        not null,
    video_id      text,
    music_id      int8,
    digg_count    int8,
    share_count   int8,
    comment_count int8,
    play_count    int8,
    is_ad         boolean,

    constraint fk_author foreign key (author_id)
        references tiktockers (tiktocker_id)
        on delete set null
        on update cascade,
    constraint fk_music foreign key (music_id)
        references music (music_id)
        on delete set null
        on update cascade,
    constraint fk_video foreign key (video_id)
        references videos (video_id)
        on delete set null
        on update cascade
);
'''
