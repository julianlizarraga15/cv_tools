import cv2
from pathlib import Path
from tqdm import tqdm
import argparse

def parse_time(time_str):
    """Parse a time string in the format HH:MM:SS into seconds.

    Args:
        time_str (str): Time string in the format HH:MM:SS.

    Returns:
        int: Total seconds.
    """
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def extract_clips(video_path, clips, output_dir):
    """Extract clips from a video and save them to the specified output directory.

    Args:
        video_path (str): Path to the input video file.
        clips (list of tuples): List of tuples where each tuple contains a start time (HH:MM:SS)
                                and duration (seconds).
        output_dir (str): Path to the directory where extracted clips will be saved.
    """
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Open video file
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    video_stem = video_path.stem  # Extracts the base name of the video file
    clip_count = 1
    
    for start, duration in tqdm(clips, desc="Extracting clips"):
        start_sec = parse_time(start)
        duration_sec = int(duration)
        
        # Set the starting point of the video
        cap.set(cv2.CAP_PROP_POS_MSEC, start_sec * 1000)
        
        # Define the output file path and video writer
        out_path = output_dir / f"{video_stem}_clip{clip_count}.mp4"
        clip_count += 1
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(out_path), fourcc, fps, 
                              (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                               int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        # Calculate the number of frames to capture
        frames_to_capture = int(duration_sec * fps)
        
        for _ in range(frames_to_capture):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        
        out.release()
    
    cap.release()

def main():
    """Main function to parse arguments and call the extract_clips function."""
    parser = argparse.ArgumentParser(description="Extract clips from a video")
    parser.add_argument("video_path", type=str, help="Path to the video file")
    parser.add_argument("clips", type=str, nargs='+', help="List of timestamp and duration tuples (e.g., '00:00:00,30')")
    parser.add_argument("--output_dir", type=str, default="clips", help="Directory to save the extracted clips")
    args = parser.parse_args()

    # Parse the clips argument into a list of tuples
    clips = [tuple(clip.split(',')) for clip in args.clips]
    
    extract_clips(args.video_path, clips, args.output_dir)

if __name__ == "__main__":
    main()
