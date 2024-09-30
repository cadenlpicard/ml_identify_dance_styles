# Dance Video Dataset

## Dataset Overview

This dataset contains videos from YouTube representing various dance styles, along with metadata for each video and extracted frames for analysis. The dance styles included are:
- Ballet
- Breakdance
- Contemporary
- Hip-Hop
- Jazz
- Salsa
- Tap
- Other (used for any additional dance styles or non-categorized videos)

The dataset is intended for research purposes, particularly for training machine learning models on tasks such as dance style classification, motion analysis, or action recognition.

---

## Data Collection Process

1. **Video Source**: 
   - Videos were collected from YouTube using the YouTube Data API.
   - The search term for each dance style was used to retrieve relevant videos (e.g., "ballet dance", "hip hop dance").
   - Only videos shorter than 4 minutes were included in the dataset to focus on concise dance segments.

2. **Video Downloading**: 
   - The videos were downloaded using the `yt-dlp` tool. The original video titles were obfuscated by assigning each video a random string as its filename.

3. **Metadata**: 
   - For each video, metadata was saved in CSV files. The metadata includes:
     - Video Title (as it appears on YouTube)
     - Video ID
     - YouTube URL
     - Duration (always short videos < 4 minutes)
     - Published Date
     - Channel Title (Uploader)
     - Description (if available)
     - View Count
     - Like Count
     - Download Status (Success or Failed)

4. **Frame Extraction**: 
   - Frames were extracted from each video using OpenCV, saving one frame for every 10 seconds of video.
   - The extracted frames were saved in separate folders for each video under the `/dance_video_frames/` directory.

---

## Dataset Structure

The dataset is organized as follows:

- **/dance_videos/**: 
  - Contains downloaded videos organized by dance style. 
  - Each folder (e.g., `/ballet/`, `/hip_hop/`) contains videos specific to that dance style.
  
  ```
  /dance_videos/
    /ballet/
      video_1.mp4
      video_2.mp4
    /hip_hop/
      video_3.mp4
  ```

- **/dance_video_frames/**: 
  - Contains frames extracted from each video, organized by dance style and video.
  
  ```
  /dance_video_frames/
    /ballet/
      /video_1/
        frame_0.jpg
        frame_1.jpg
    /hip_hop/
      /video_3/
        frame_0.jpg
        frame_1.jpg
  ```

- **/metadata/**: 
  - Contains CSV files with video metadata for each dance style.

  ```
  /metadata/
    ballet_metadata.csv
    hip_hop_metadata.csv
  ```

---

## Metadata Description

The metadata CSV files contain the following fields for each video:

| Field           | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| Title           | The original title of the video on YouTube                                  |
| Video ID        | The unique ID assigned to the video by YouTube                              |
| URL             | The full URL of the YouTube video                                           |
| Duration        | Indicates that the video is shorter than 4 minutes                          |
| Published Date  | The date when the video was published on YouTube                            |
| Channel Title   | The name of the YouTube channel that uploaded the video                     |
| Description     | The video description (if available)                                        |
| View Count      | The number of views the video has on YouTube                                |
| Like Count      | The number of likes the video has on YouTube                                |
| Download Status | Status indicating whether the video was successfully downloaded (Success/Failed) |

---

## Frame Extraction Details

- **Frame Rate**: One frame was extracted every 10 seconds from each video. The extracted frames are saved as `.jpg` images.
- **Directory Structure**: Each video has its own folder under the dance style directory, and each folder contains all the extracted frames from the video.

---

## Dataset Instances

- **Total Videos**: The dataset includes 100 videos for each dance style.
- **Total Instances**: Each instance represents a dance video, along with its metadata and extracted frames.
- **Frames**: For each video, approximately one frame every 10 seconds was extracted, depending on the video’s length.

---

## Potential Uses

- **Dance Style Classification**: This dataset can be used to train machine learning models that classify videos by dance style.
- **Motion Analysis**: Researchers can analyze the body movements and choreographic styles represented in the extracted frames.
- **Action Recognition**: The frames can be used for developing action recognition algorithms or understanding dance dynamics.

---

## License

This dataset is provided for research and educational purposes. Users must comply with YouTube's terms of service when using or distributing the videos.

---

## Contact

For any questions or issues regarding this dataset, please contact **Caden Picard** at [clpicard@umich.edu](mailto:clpicard@umich.edu).

---

This `README.md` provides a comprehensive overview of the dataset, including how it was collected, its structure, and potential use cases.
