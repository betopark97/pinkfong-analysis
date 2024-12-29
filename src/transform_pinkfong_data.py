# System
from pathlib import Path

# DataFrame
import pandas as pd


# Load Data
def load_csv_files(data_path: str, extension=".csv"):
    # Define the file paths for your CSV files
    csv_files = {}
    data_files = Path(data_path).glob(f'*{extension}')  # Using pathlib to filter files by extension

    for file_path in data_files:
        table_name = file_path.stem  # Extract the file name without the extension
        csv_files[table_name] = file_path  # Store the full file path in the dictionary

    return csv_files

# Normalize channel metadata and statistics
def normalize_channel_data(df_channel_data):
    # 1. Separate channel metadata and statistics
    channel_metadata_columns = [
        'channel_id',
        'channel_title',
        'description',
        'profile_picture',
        'published_at',
        'country',
        'playlist_id'
    ]
    channel_statistics_columns = [
        'channel_id',
        'subscriber_count',
        'video_count',
        'view_count'
    ]
    df_channel_metadata = df_channel_data[channel_metadata_columns]
    df_channel_stats = df_channel_data[channel_statistics_columns]
    return df_channel_metadata, df_channel_stats

# Normalize video metadata and statistics
def normalize_video_data(df_video_stats):
    # 1. Separate video metadata and statistics
    video_metadata_columns = [
        'video_id',
        'published_at',
        'title',
        'description',
        'thumbnails',
        'tags',
        'category_id',
        'default_audio_language',
        'duration'
    ]
    video_statistics_columns = [
        'video_id',
        'view_count',
        'like_count',
        'comment_count'
    ]
    df_video_metadata = df_video_stats[video_metadata_columns]
    df_video_stats = df_video_stats[video_statistics_columns]
    return df_video_metadata, df_video_stats

# Normalize Tags in video_stats
def normalize_video_tags(df_video_metadata):
    # Clean the 'tags' column (convert string representation to lists)
    df_video_metadata["tags"] = df_video_metadata["tags"].apply(lambda x: eval(x) if isinstance(x, str) else (x if isinstance(x, list) else []))

    # Flatten all tags into a single list with corresponding video_id
    tags_flat = []
    for _, row in df_video_metadata.iterrows():
        video_id = row["video_id"]
        tags = row["tags"]
        tags_flat.extend([(video_id, tag) for tag in tags])

    # Create a DataFrame for the flattened tags
    df_flattened_tags = pd.DataFrame(tags_flat, columns=["video_id", "tag"])

    # Create a unique tags table
    df_unique_tags = pd.DataFrame(df_flattened_tags["tag"].unique(), columns=["tag"]).reset_index()
    df_unique_tags.rename(columns={"index": "tag_id"}, inplace=True)

    # Map tags to their tag_id
    df_tags_mapped = df_flattened_tags.merge(df_unique_tags, on="tag", how="left")

    # Final normalized DataFrames
    df_video_tags = df_tags_mapped[["video_id", "tag_id"]]
    df_tags = df_unique_tags
    
    return df_video_tags, df_tags


def main():
    # Load Data
    csv_data_paths = load_csv_files('../data/raw/')
    df_channel_data = pd.read_csv(csv_data_paths['channel_data'])
    df_channels = pd.read_csv(csv_data_paths['channels'])
    df_playlist_videos = pd.read_csv(csv_data_paths['playlist_videos'])
    df_video_categories = pd.read_csv(csv_data_paths['video_categories'])
    df_video_stats = pd.read_csv(csv_data_paths['video_stats'])


    # Normalize Data
    # 1. Separate channel metadata and statistics
    df_channel_metadata, df_channel_stats = normalize_channel_data(df_channel_data)
    
    # 2. Separate video metadata and statistics
    df_video_metadata, df_video_stats = normalize_video_data(df_video_stats)

    # 3. Normalize Tags in video_stats
    df_video_tags, df_tags = normalize_video_tags(df_video_metadata)


    # Denormalize Data
    # 1. Combine channel table with channel_metadata
    df_channel_metadata = pd.merge(df_channel_metadata, df_channels, on='channel_id').rename(columns={'youtube_link': 'channel_link'})


    # Save new tables to interim directory
    df_channel_metadata.to_csv('../data/interim/channel_metadata.csv', header=True, index=False)
    df_channel_stats.to_csv('../data/interim/channel_stats.csv', header=True, index=False)
    df_playlist_videos.to_csv('../data/interim/playlist_videos.csv', header=True, index=False)
    df_video_metadata.to_csv('../data/interim/video_metadata.csv', header=True, index=False)
    df_video_stats.to_csv('../data/interim/video_stats.csv', header=True, index=False)
    df_video_tags.to_csv('../data/interim/video_tags.csv', header=True, index=False)
    df_tags.to_csv('../data/interim/tags.csv', header=True, index=False)
    df_video_categories.to_csv('../data/interim/video_categories.csv', header=True, index=False)
    
    
if __name__ == "__main__":
    main()    