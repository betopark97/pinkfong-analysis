import os

import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def get_top_kids_channels() -> list:
    url = 'https://youtube-rank.com/board/bbs/board.php?bo_table=youtube&sca=키즈/어린이'
    response = requests.get(url)
    html_content = response.text
    
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Use a CSS selector to target <a> tags inside <h1>, inside <td class="subject">
    target_links = soup.select('td.subject > h1 > a')

    # Extract the channel names
    channel_names = [link.get_text(strip=True) for link in target_links]

    return channel_names
        
# When given a handler (channel name), it returns a channel_id
def get_channel_id(channel_name: str) -> str:
    youtube_api_key = os.environ.get('YOUTUBE_API_KEY2')
    api_service_name = 'youtube'
    api_version = 'v3'
    
    # Build the YouTube API client
    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey=youtube_api_key
    )
    
    # Create a search request for the given channel name
    search_request = youtube.search().list(
        part='snippet',
        q=channel_name,
        type='channel',
        maxResults=1  # Fetch only the most relevant result
    )
    
    # Execute the search request and get the response
    search_response = search_request.execute()
    
    # Iterate over the items in the search response
    for item in search_response['items']:
        # Extract and return the channelId from the 'id' dictionary
        if 'channelId' in item['id']:
            return item['id']['channelId']
    
    # Return None if no channel ID is found
    return None

# When given a channel_id it gives a row of channel stats
def get_channel_stats(channel_id: str) -> pd.DataFrame:
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

def get_channel_stats_in_chunks(channel_ids_list: list, chunk_size: int=50) -> pd.DataFrame:
    # Split the channel IDs into chunks
    chunks = [channel_ids_list[i:i + chunk_size] for i in range(0, len(channel_ids_list), chunk_size)]
    
    # Empty list to store DataFrames for each chunk
    all_stats_dataframes = []
    
    # Iterate through each chunk
    for chunk in chunks:
        print(f"Processing chunk: {chunk}")
        try:
            # Join video IDs into a single string for API call
            channel_ids = ','.join(chunk)
            channel_stats_df = get_channel_stats(channel_ids)
            print(f"Fetched stats for {len(chunk)} channels.")
            all_stats_dataframes.append(channel_stats_df)
        except Exception as e:
            print(f"Error fetching stats for chunk {chunk}: {e}")
    
    # Combine all the DataFrames into one
    if all_stats_dataframes:
        combined_stats_df = pd.concat(all_stats_dataframes, ignore_index=True)
    else:
        combined_stats_df = pd.DataFrame()  # Handle case where no data is fetched
    
    return combined_stats_df



def main():
    # Load env variables from .env
    load_dotenv()
    
    # Get top kids channels in a list
    channel_names = get_top_kids_channels()
    print(f"{channel_names = }")
    
    # Get channel ids
    channel_ids = [get_channel_id(channel_name) for channel_name in channel_names]
    print(f"{channel_ids = }")
    
    # Make a dataframe to save the channel names and ids
    df_channel_names_ids = pd.DataFrame({'channel_name': channel_names, 'channel_id': channel_ids})
    print(f"{df_channel_names_ids = }")
    
    # Save the dataframe
    df_channel_names_ids.to_csv('../data/external/top_kids_channels.csv', header=True, index=False)
    
    # Get channel ids as list
    df_channel_names_ids = pd.read_csv('../data/external/top_kids_channels.csv')
    channel_ids_list = df_channel_names_ids['channel_id'].tolist()
    print(f"{channel_ids_list = }")
    
    # Get channel stats in chunks    
    df_channel_stats = get_channel_stats_in_chunks(channel_ids_list)
    print(f"{df_channel_stats = }")
    
    # Save the dataframe
    df_channel_stats.to_csv('../data/external/top_kids_channel_stats.csv', header=True, index=False)
    

if __name__ == "__main__":
    main()