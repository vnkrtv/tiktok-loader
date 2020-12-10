DB_SCHEMA = '''
CREATE TABLE IF NOT EXISTS tiktokers
(
    tiktoker_id    text,
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

    constraint pk_users primary key (tiktoker_id)
);

CREATE TABLE IF NOT EXISTS music
(
    music_id    text,
    author_name text,
    title       text,
    play_url    text,
    duration    int4,
    album       text,
    
    constraint pk_music primary key (music_id)
);

CREATE TABLE IF NOT EXISTS videos
(
    video_id    text,
    height      int4,
    width       int4,
    ratio       text,
    cover       text,
    duration    int4,
    
    constraint pk_video primary key (video_id)
);

CREATE TABLE IF NOT EXISTS tiktoks
(
    tiktok_id     text,
    create_time   timestamp
        not null,
    description   text,
    author_id     text
        not null,
    video_id      text,
    music_id      text,
    digg_count    int8,
    share_count   int8,
    comment_count int8,
    play_count    int8,
    is_ad         boolean,
    
    constraint pk_tiktok primary key (tiktok_id),

    constraint fk_author foreign key (author_id)
        references tiktokers (tiktoker_id)
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
