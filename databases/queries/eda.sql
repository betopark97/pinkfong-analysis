SELECT
	CASE 
        WHEN cm.channel_character = '핑크퐁' THEN 'Pinkfong'
        WHEN cm.channel_character = '올리' THEN 'Ollie'
        WHEN cm.channel_character = '베베핀' THEN 'Bebefinn'
    END AS channel_character
	,vm.published_at
	,vm.duration
	,vc.category_name
	,vs.view_count
	,vs.like_count
	,vm.title
	,vm.description
FROM video_metadata vm
JOIN video_stats vs
	ON vm.video_id = vs.video_id
JOIN playlist_videos pv
	ON vm.video_id = pv.video_id
JOIN channel_metadata cm
	ON cm.playlist_id = pv.playlist_id
JOIN video_categories vc
	ON vm.category_id = vc.category_id