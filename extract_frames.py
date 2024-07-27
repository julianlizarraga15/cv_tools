import cv2
import argparse
from tqdm import tqdm
from pathlib import Path

def extract_frames(video_file, output_dir, interval=30, display=False):
    """
    Extract frames from a video at a specified interval and save them in a specified directory structure,
    while displaying the video frames.

    Parameters:
    video_file: Path to the video file.
    output_dir: Directory where frames will be saved.
    interval: Interval between frames to extract.
    display: Whether to display the video frames.
    """
    video_file = Path(video_file)
    output_dir = Path(output_dir)

    print(f"Attempting to open video at: {video_file}")

    # Check if the video file actually exists
    if not video_file.is_file():
        print("The video file does not exist at the specified path!")
        return

    if not output_dir.is_dir():
        output_dir.mkdir(parents=True, exist_ok=True)

    vidcap = cv2.VideoCapture(str(video_file))
    if not vidcap.isOpened():
        print("Failed to open video file!")
        return

    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    count = 0
    saved_count = 0

    with tqdm(total=total_frames, desc="Extracting frames") as pbar:
        success, frame = vidcap.read()
        while success:
            if frame is not None:
                if count % interval == 0:
                    frame_path = output_dir / f"{video_file.stem}_frame{saved_count + 1}.jpg"
                    cv2.imwrite(str(frame_path), frame)
                    saved_count += 1

                # Show the frame
                if display:
                    cv2.imshow('Video', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit the video display
                        break
            else:
                print(f"No frame retrieved at count {count}")
                break

            success, frame = vidcap.read()
            count += 1
            pbar.update(1)

    vidcap.release()
    cv2.destroyAllWindows()  # Close all OpenCV windows
    print(f"Extracted {saved_count} frames from the video.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from a video file.")
    parser.add_argument("video_file", type=str, help="Path to the video file.")
    parser.add_argument("output_dir", type=str, help="Directory where frames will be saved.")
    parser.add_argument("--interval", type=int, default=30, help="Interval between frames to extract.")
    parser.add_argument("--display", action='store_true', help="Whether to display the video while extracting the frames.")

    args = parser.parse_args()

    extract_frames(args.video_file, args.output_dir, args.interval, args.display)
