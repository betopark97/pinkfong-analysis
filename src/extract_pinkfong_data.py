import os

import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
from dotenv import load_dotenv


# When given a handle, it returns a channel_id
def get_channel_id(handle: str) -> str:
    youtube_api_key = os.environ.get('YOUTUBE_API_KEY1')
    api_service_name = 'youtube'
    api_version = 'v3'
    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey=youtube_api_key
    )
    # Create a search request for the given handle
    search_request = youtube.search().list(
        part='snippet',
        q=handle,
        type='channel'
    )
    # Execute the search request and get the response
    search_response = search_request.execute()
    # Iterate over the items in the search response
    for item in search_response['items']:
        # Check if the 'channelId' key is present in the 'snippet' dictionary
        if 'channelId' in item['snippet']:
            # Return the channel ID if found
            return item['snippet']['channelId']
    # Return None if no channel ID is found
    return None

# Create a dataframe for the channels table
def create_channels_df(channel_data: dict) -> pd.DataFrame:
    # Create a new list to store the channel information along with channel ids and YouTube links
    channel_data_with_info = {
        'channel_character': channel_data['channel_character'],
        'channel_handle': channel_data['channel_handle'],
        'channel_id': [],
        'youtube_link': []
    }

    # For each handle, get the channel_id, construct the YouTube link, and add them to the lists
    for handle in channel_data['channel_handle']:
        channel_id = get_channel_id(handle)
        youtube_link = f'https://www.youtube.com/channel/{channel_id}' if channel_id else None
        channel_data_with_info['channel_id'].append(channel_id)
        channel_data_with_info['youtube_link'].append(youtube_link)

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(channel_data_with_info)

    # Return the DataFrame
    return df

# When given a channel_id it gives a row of channel stats
def get_channel_data(channel_id: str) -> pd.DataFrame:
    youtube_api_key = os.environ.get('YOUTUBE_API_KEY1')
    api_service_name = 'youtube'
    api_version = 'v3'
    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey=youtube_api_key
    )
    # Create a request for the channel statistics of the given channel ID
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=channel_id
    )
    # Execute the request and get the response
    response = request.execute()
    
    # Loop through the necessary items and make a Dataframe
    df_data = []
    for item in response['items']:
        data = {
            'channel_id':item.get('id'),
            'channel_title': item['snippet'].get('title'),
            'description': item['snippet'].get('description'),
            'profile_picture': item['snippet']['thumbnails']['default'].get('url'),
            'published_at':item['snippet'].get('publishedAt'),
            'country':item['snippet'].get('country'),
            'playlist_id':item['contentDetails']['relatedPlaylists'].get('uploads'),
            'view_count':item['statistics'].get('viewCount'),
            'subscriber_count':item['statistics'].get('subscriberCount'),
            'video_count':item['statistics'].get('videoCount'),
        }
        df_data.append(data)
    df = pd.DataFrame(df_data)
    
    # Return the Pandas Dataframe
    return df

# Create a dataframe for the channel_data table
def create_channel_data_df(channel_ids: list) -> pd.DataFrame:
    # Initialize an empty list to collect DataFrames
    df_list = []
    
    # Iterate over each channel_id in the list
    for channel_id in channel_ids:
        # Get the DataFrame for each channel_id using the existing get_channel_data function
        df_channel = get_channel_data(channel_id)
        
        # Append the resulting DataFrame to the list
        df_list.append(df_channel)
    
    # Concatenate all DataFrames in the list vertically (along axis 0)
    result_df = pd.concat(df_list, ignore_index=True)
    
    # Return the final concatenated DataFrame
    return result_df

# When given a playlist_id it returns a list of video_ids
def get_video_ids(playlist_id: str) -> list:
    youtube_api_key = os.environ.get('YOUTUBE_API_KEY1')
    api_service_name = 'youtube'
    api_version = 'v3'
    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey=youtube_api_key
    )
    video_ids = []
    next_page_token = None
    
    while True:
        request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return video_ids

# Create a dataframe for the playlist_videos table
def create_playlist_videos_df(playlist_ids: list) -> pd.DataFrame:
    video_data = []  # List to store data as dictionaries

    # Loop through each playlist_id in the input list
    for playlist_id in playlist_ids:
        # Get video IDs for the current playlist_id
        video_ids = get_video_ids(playlist_id)
        
        # Append each video_id along with the playlist_id to the video_data list
        for video_id in video_ids:
            video_data.append({'playlist_id': playlist_id, 'video_id': video_id})

    # Create a DataFrame from the collected video data
    df = pd.DataFrame(video_data)

    return df

# Function to fetch video statistics for a single video
def get_video_stats(video_id: str) -> pd.DataFrame:
    youtube_api_key = os.environ.get('YOUTUBE_API_KEY1')
    api_service_name = 'youtube'
    api_version = 'v3'
    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey=youtube_api_key
    )
    request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=video_id
    )
    response = request.execute()
    df_data = []
    for item in response['items']:
        data = {
            'video_id':item.get('id'),
            'published_at':item['snippet'].get('publishedAt'),
            'title':item['snippet'].get('title'),
            'description':item['snippet'].get('description'),
            'thumbnails':item['snippet']['thumbnails']['default'].get('url'),
            'tags':item['snippet'].get('tags'),
            'category_id':item['snippet'].get('categoryId'),
            'default_audio_language':item['snippet'].get('defaultAudioLanguage'),
            'duration':item['contentDetails'].get('duration'),
            'view_count':item['statistics'].get('viewCount'),
            'like_count':item['statistics'].get('likeCount'),
            'comment_count':item['statistics'].get('commentCount'),
        }
        df_data.append(data)
    df = pd.DataFrame(df_data)
    
    return df

# Function to fetch video statistics for a list of video IDs
def get_video_stats_in_chunks(video_ids_list: list, chunk_size: int=50):
    # Split the video IDs into chunks
    chunks = [video_ids_list[i:i + chunk_size] for i in range(0, len(video_ids_list), chunk_size)]
    
    # Empty list to store DataFrames for each chunk
    all_stats_dataframes = []
    
    # Iterate through each chunk
    for chunk in chunks:
        print(f"Processing chunk: {chunk}")
        try:
            # Join video IDs into a single string for API call
            video_ids = ','.join(chunk)
            video_stats_df = get_video_stats(video_ids)
            print(f"Fetched stats for {len(chunk)} videos.")
            all_stats_dataframes.append(video_stats_df)
        except Exception as e:
            print(f"Error fetching stats for chunk {chunk}: {e}")
    
    # Combine all the DataFrames into one
    if all_stats_dataframes:
        combined_stats_df = pd.concat(all_stats_dataframes, ignore_index=True)
    else:
        combined_stats_df = pd.DataFrame()  # Handle case where no data is fetched
    
    return combined_stats_df

# Function to fetch video categories
def get_video_category_names(region_code: str) -> pd.DataFrame:
    youtube_api_key = os.environ.get('YOUTUBE_API_KEY1')
    api_service_name = 'youtube'
    api_version = 'v3'
    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey=youtube_api_key
    )
    request = youtube.videoCategories().list(
        part='snippet',
        regionCode=region_code
    )
    response = request.execute()
    df_data = []
    for item in response['items']:
        data = {
            'category_id':item.get('id'),
            'category_name':item['snippet'].get('title')
        }
        df_data.append(data)
    df = pd.DataFrame(df_data)
    
    return df

def main():
    # Load env variables from .env
    load_dotenv()
    
    # Create the channels table
    channel_data = {
        'channel_character': ['핑크퐁', '올리', '베베핀'],
        'channel_handle': ['@핑크퐁', '@BabyShark_Korean', '@베베핀']
    }
    df_channels = create_channels_df(channel_data)
    df_channels.to_csv('../data/raw/channels.csv', header=True, index=False)
    
    # Create the channel_data table
    channel_ids = pd.read_csv('../data/raw/channels.csv')['channel_id'].tolist()
    df_channel_data = create_channel_data_df(channel_ids)
    df_channel_data.to_csv('../data/raw/channel_data.csv', header=True, index=False)

    # Create the playlist_videos table
    playlist_ids = pd.read_csv('../data/raw/channel_data.csv')['playlist_id'].tolist()
    df_playlist_videos = create_playlist_videos_df(playlist_ids)
    df_playlist_videos.to_csv('../data/raw/playlist_videos.csv', header=True, index=False)

    # Create the video_stats table
    video_ids = pd.read_csv('../data/raw/playlist_videos.csv')['video_id'].tolist()
    df_video_stats = get_video_stats_in_chunks(video_ids)
    df_video_stats.to_csv('../data/raw/video_stats.csv', header=True, index=False)
    
    # Create the video_categories table
    df_video_categories = get_video_category_names('KR')
    df_video_categories.to_csv('../data/raw/video_categories.csv', header=True, index=False)


if __name__ == "__main__":
    main()