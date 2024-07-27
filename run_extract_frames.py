import os
import argparse
from extract_frames import extract_frames

def main(clips_folder, output_folder, interval=30):
    """
    Run extract_frames() for each video in a given folder.
    """
    for filename in os.listdir(clips_folder):
        if filename.endswith(".mp4"):
            video_path = os.path.join(clips_folder, filename)
            extract_frames(video_path, output_folder, interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from videos in a folder.")
    parser.add_argument("clips_folder", type=str, help="Path to the folder containing video clips.")
    parser.add_argument("output_folder", type=str, help="Path to the folder where extracted frames will be saved.")
    parser.add_argument("--interval", type=int, default=30, help="Interval between frames to extract.")
    
    args = parser.parse_args()
    
    main(args.clips_folder, args.output_folder, args.interval)
