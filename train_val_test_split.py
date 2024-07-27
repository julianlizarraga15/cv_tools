import os
import random
import shutil
import re
from collections import defaultdict
import argparse


def extract_video_id(file_name):
    # Updated regex pattern to capture the video ID in the provided format
    pattern = re.compile(r'(.+_clip\d+)_frame\d+_jpg\.rf\..+')
    match = pattern.search(file_name)
    if match:
        return match.group(1)
    return None

def train_val_test_split(source_dir, target_dir, split_dict, seed):
    
    source_dir_images = os.path.join(source_dir, 'images')
    source_dir_labels = os.path.join(source_dir, 'labels')

    # List all files in source_dir_images
    source_images = os.listdir(source_dir_images)

    # Group images by video ID
    video_dict = defaultdict(list)
    for image in source_images:
        video_id = extract_video_id(image)
        if video_id:
            video_dict[video_id].append(image)
    
    # Shuffle the list of video IDs to randomize the splitting
    video_ids = list(video_dict.keys())
    random.seed(seed)
    random.shuffle(video_ids)

    # Determine the splitting points
    train_ideal_final_idx = int(len(video_ids) * split_dict['train'])
    valid_ideal_final_idx = int(len(video_ids) * (split_dict['train'] + split_dict['valid']))

    # Create train, validation and test directories
    for dataset in ['train', 'valid', 'test']:
        images_path = os.path.join(target_dir, dataset, 'images')
        labels_path = os.path.join(target_dir, dataset, 'labels')
        os.makedirs(images_path, exist_ok=True)
        os.makedirs(labels_path, exist_ok=True)
        print(f'Created directories: {images_path}, {labels_path}')

    train_count = 0
    valid_count = 0
    test_count = 0

    # Split videos into train, validation, and test sets
    for idx, video_id in enumerate(video_ids):
        if idx < train_ideal_final_idx:
            split = 'train'
        elif idx < valid_ideal_final_idx:
            split = 'valid'
        else:
            split = 'test'
        
        for image in video_dict[video_id]:
            image_path = os.path.join(source_dir_images, image)
            label_path = os.path.join(source_dir_labels, image.replace('.jpg', '.txt'))

            target_image_path = os.path.join(target_dir, split, 'images', os.path.basename(image_path))
            target_label_path = os.path.join(target_dir, split, 'labels', os.path.basename(label_path))

            shutil.copy(image_path, target_image_path)
            shutil.copy(label_path, target_label_path)

            if split == 'train':
                train_count += 1
            elif split == 'valid':
                valid_count += 1
            else:
                test_count += 1

    full_count = len(source_images)
    train_percent = round((train_count / full_count) * 100)
    valid_percent = round((valid_count / full_count) * 100)
    test_percent = round((test_count / full_count) * 100)

    print(
        f'Copied {train_count} ({train_percent}%) train images, '
        f'{valid_count} ({valid_percent}%) validation images, '
        f'and {test_count} ({test_percent}%) test images '
        f'for a total of {train_count + valid_count + test_count} images.'
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split video frames into train, validation, and test sets")
    parser.add_argument("source_dir", type=str, help="Source directory containing images and labels")
    parser.add_argument("target_dir", type=str, help="Target directory to save the split datasets")
    parser.add_argument("--train_split", type=float, default=0.85, help="Proportion of data to be used for training")
    parser.add_argument("--valid_split", type=float, default=0.15, help="Proportion of data to be used for validation")
    parser.add_argument("--test_split", type=float, default=0.0, help="Proportion of data to be used for testing")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for shuffling the data")

    args = parser.parse_args()

    split_dict = {
        'train': args.train_split,
        'valid': args.valid_split,
        'test': args.test_split
    }

    train_val_test_split(args.source_dir, args.target_dir, split_dict, args.seed)

# Example run
# python .\utils\train_val_test_split.py `
#     "C:/Users/julian/Documents/Workspace/juan_house_in_yolo_format/train" `
#     "C:/Users/julian/Documents/Workspace/yolo-test/data/juan_house_yolo_format" `
#     --train_split 0.85 `
#     --valid_split 0.15 `
#     --test_split 0.0 `
#     --seed 42