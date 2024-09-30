import os
import random
import string
import time
import csv
import subprocess
import cv2
import shutil
from googleapiclient.discovery import build

# Set up YouTube API
def setup_youtube_api():
    api_key = 'AIzaSyAOfZGWcCVzyFFE_wF6DFZ6CPsoYgxlyzc'
    return build('youtube', 'v3', developerKey=api_key)

# Create a directory if it doesn't exist
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Download videos for manual annotation
def download_videos(search_term, output_folder, desired_video_count=100):
    youtube = setup_youtube_api()
    create_directory(output_folder)
    
    downloaded_videos = 0
    next_page_token = None
    print(f"Starting to collect {desired_video_count} videos.")

    while downloaded_videos < desired_video_count:
        request = youtube.search().list(
            q=search_term,
            part="snippet",
            type="video",
            maxResults=50,
            videoDuration="short",  # Filter for videos shorter than 4 minutes
            pageToken=next_page_token
        )

        response = request.execute()

        total_videos = len(response['items'])
        print(f"Found {total_videos} videos in this batch.")

        for idx, item in enumerate(response['items']):
            video_title = item['snippet']['title']

            # Skip videos with "CoComelon" in the title
            if "CoComelon" in video_title:
                print(f"Skipping video {idx + 1} with title containing 'CoComelon': {video_title}")
                continue

            if downloaded_videos >= desired_video_count:
                break

            video_id = item['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # Obfuscate video title
            random_title = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            output_path = os.path.join(output_folder, f'{random_title}.%(ext)s')

            try:
                print(f"Starting download for {video_url} as {random_title} ({downloaded_videos + 1}/{desired_video_count})...")
                subprocess.run(['yt-dlp', '-o', output_path, video_url], check=True, timeout=60)

                elapsed_time = time.time() - start_time
                print(f"Successfully downloaded {random_title} in {elapsed_time:.2f} seconds.")
                downloaded_videos += 1
            except subprocess.TimeoutExpired:
                print(f"Download timed out for video {video_id}. Skipping.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to download video {video_id}: {e}")

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            print("No more videos available.")
            break

    print(f"Download process completed. {downloaded_videos} videos successfully downloaded.")

# Download videos based on an array of dance types
def download_videos_by_dance_styles(dances, output_base_folder):
    youtube = setup_youtube_api()

    for dance_style in dances:
        search_term = f"{dance_style} dance"
        output_folder = os.path.join(output_base_folder, dance_style.replace(" ", "_").lower())
        create_directory(output_folder)

        csv_file = os.path.join(output_folder, 'video_metadata.csv')
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'VideoID', 'URL', 'Duration', 'PublishedDate', 'ChannelTitle', 'Description', 'ViewCount', 'LikeCount', 'DownloadStatus'])

            request = youtube.search().list(
                q=search_term,
                part="snippet",
                type="video",
                maxResults=100,
                videoDuration="short"
            )

            response = request.execute()

            for item in response['items']:
                video_title = item['snippet']['title']
                video_id = item['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                published_date = item['snippet']['publishedAt']
                channel_title = item['snippet']['channelTitle']
                description = item['snippet']['description']

                video_request = youtube.videos().list(part="statistics", id=video_id)
                video_response = video_request.execute()

                view_count = video_response['items'][0]['statistics'].get('viewCount', 'N/A')
                like_count = video_response['items'][0]['statistics'].get('likeCount', 'N/A')

                print(f"Title: {video_title}, Views: {view_count}, Likes: {like_count}")

                try:
                    subprocess.run(['yt-dlp', '-o', os.path.join(output_folder, '%(title)s.%(ext)s'), video_url], check=True)
                    download_status = 'Success'
                except subprocess.CalledProcessError as e:
                    print(f"Failed to download {video_title}: {e}")
                    download_status = 'Failed'

                writer.writerow([video_title, video_id, video_url, "Short (< 4 min)", published_date, channel_title, description, view_count, like_count, download_status])

# Extract frames from videos
def extract_frames(input_base_folder, output_base_folder, dances, frame_interval=10, time_limit=120):
    create_directory(output_base_folder)

    for dance_style in dances:
        input_folder = os.path.join(input_base_folder, dance_style.replace(" ", "_").lower())
        output_folder = os.path.join(output_base_folder, dance_style.replace(" ", "_").lower())

        create_directory(output_folder)

        for video_name in os.listdir(input_folder):
            video_path = os.path.join(input_folder, video_name)
            video_output_folder = os.path.join(output_folder, video_name.split('.')[0])

            if os.path.exists(video_output_folder):
                print(f"Skipping {video_name} as frames already exist.")
                continue

            create_directory(video_output_folder)
            print(f"Extracting frames from {video_name} in {dance_style}...")
            extract_frames_from_video(video_path, video_output_folder, frame_interval, time_limit)

def extract_frames_from_video(video_path, frame_output_dir, frame_interval=10, time_limit=120):
    cap = cv2.VideoCapture(video_path)
    count = 0
    frame_count = 0
    start_time = time.time()

    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    while cap.isOpened():
        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            print(f"Frame extraction from {video_path} exceeded time limit of {time_limit} seconds. Skipping.")
            break

        ret, frame = cap.read()
        if not ret:
            break

        if count % frame_interval == 0:
            frame_filename = os.path.join(frame_output_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_filename, frame)
            frame_count += 1

        count += 1

    cap.release()

# Copy files to Google Drive
def copy_files(source_dir, destination_dir):
    create_directory(destination_dir)

    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        destination_path = os.path.join(destination_dir, relative_path)
        create_directory(destination_path)

        for file_name in files:
            source_file = os.path.join(root, file_name)
            destination_file = os.path.join(destination_path, file_name)

            if not os.path.exists(destination_file):
                print(f"Copying {source_file} to {destination_file}")
                shutil.copy2(source_file, destination_file)
            else:
                print(f"File already exists: {destination_file}")

# Main Execution Example
if __name__ == "__main__":
    # Example usage of the functions
    output_folder = "/content/dance_videos/videos_for_annotation/"
    download_videos("dance video", output_folder)

    dances = ["ballet", "breakdance", "contemporary", "hip hop", "jazz", "salsa", "tap"]
    download_videos_by_dance_styles(dances, "/content/dance_videos/")

    extract_frames("/content/dance_videos/", "/content/dance_video_frames/", dances)

    # Copy files to Google Drive
    copy_files('/content/dance_videos/', '/content/drive/My Drive/ML Project - Dance Videos/dance_videos/')
    copy_files('/content/dance_video_frames/', '/content/drive/My Drive/ML Project - Dance Videos/dance_video_frames/')
