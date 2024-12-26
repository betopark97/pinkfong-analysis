import os
import googleapiclient.discovery

def get_channel_id_by_handle(handle: str) -> str:
    # Ensure the handle starts with '@'
    if not handle.startswith('@'):
        handle = '@' + handle

    # Initialize the YouTube API client
    youtube_api_key = os.environ.get('YOUTUBE_API_KEY3')
    youtube = googleapiclient.discovery.build(
        'youtube', 'v3', developerKey=youtube_api_key)

    # Search for the channel using the handle
    request = youtube.search().list(
        part='snippet',
        q=handle,
        type='channel',
        maxResults=1
    )
    response = request.execute()

    # Extract and return the channel ID
    if response['items']:
        return response['items'][0]['snippet']['channelId']
    else:
        return None

# Example usage
channel_handle = '@BabyBusKo'
channel_id = get_channel_id_by_handle(channel_handle)
print(f'The channel ID for {channel_handle} is {channel_id}')