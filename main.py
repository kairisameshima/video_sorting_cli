import sys
import os
from video_sorting_cli.sorting_pattern import key_to_directory
from video_sorting_cli.video_sorter.video_sorter import VideoSorter

if __name__ == "__main__":
    directory = sys.argv[1]

    # Check if the source directory exists
    if not os.path.isdir(directory):
        print(f"Directory {directory} does not exist.")
        exit(1)

    # Check if destination directories exist
    for key, dest_dir in key_to_directory.items():
        if not os.path.isdir(dest_dir):
            print(f"Destination directory for key '{key}' ({dest_dir}) does not exist.")
            exit(1)

    # Process the directory
    sorter = VideoSorter(directory, key_to_directory)
    sorter.sort_directory()
