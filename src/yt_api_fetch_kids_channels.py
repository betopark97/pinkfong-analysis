import os
from dotenv import load_dotenv
import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors



# Function to fetch top YouTube channels
def fetch_top_kids_channels(max_results: int=50) -> pd.DataFrame:
    # Youtube builder parameters
    youtube_api_key = os.environ.get('YOUTUBE_API_KEY1')
    api_service_name = 'youtube'
    api_version = 'v3'
    # Youtube API fetching builder
    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey=youtube_api_key
    )

    # Initialize empty list for holding the channel names    
    channels_data = []
    
    # Search for channels
    request = youtube.search().list(
        part='snippet',
        type='channel',
        regionCode='KR',
        # videoCaption='ko',
        relevanceLanguage='ko',
        q='kids',
        maxResults=max_results
    )
    response = request.execute()
    
    # Fetch channel details
    for item in response.get('items', []):
        channel_id = item['id']['channelId']
        channel_title = item['snippet']['title']
        
        # Get channel statistics
        channel_request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        channel_response = channel_request.execute()
        
        for channel in channel_response.get('items', []):
            data = {
                "channel_id": channel_id,
                "channel_title": channel_title,
                "subscribers": int(channel['statistics'].get('subscriberCount', 0)),
                "total_views": int(channel['statistics'].get('viewCount', 0)),
                "video_count": int(channel['statistics'].get('videoCount', 0)),
                "description": channel['snippet'].get('description', ''),
            }
            channels_data.append(data)
    
    # Create DataFrame
    df = pd.DataFrame(channels_data)
    
    # Sort by subscriber count
    df = df.sort_values(by='subscribers', ascending=False).reset_index(drop=True)
    
    return df

def main():
    # Load env variables from .env
    load_dotenv()
    
    # Fetch top YouTube channels
    top_channels = fetch_top_kids_channels()
    print(top_channels)
    
    # Save top YouTube channels to CSV
    top_channels.to_csv('../data/external/top_kids_channels_south_korea.csv', header=True, index=False)


if __name__ == "__main__":
    main()