SELECT
    CASE 
        WHEN channel_character = '핑크퐁' THEN 'Pinkfong'
        WHEN channel_character = '올리' THEN 'Ollie'
        WHEN channel_character = '베베핀' THEN 'Bebefinn'
    END AS channel_character,
    subscriber_count,
    video_count,
    view_count,
    subscriber_count::float / view_count AS subscriber_to_views,
    view_count::float / video_count AS avg_views_per_video,
    view_count::float / subscriber_count AS views_to_subscriber_ratio
FROM channel_stats s
JOIN channel_metadata m
    ON s.channel_id = m.channel_id