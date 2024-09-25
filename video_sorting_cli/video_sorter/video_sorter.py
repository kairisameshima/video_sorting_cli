import os
import shutil
import subprocess
from pathlib import Path

from tqdm import tqdm

from .interface import VideoSorterInterface


class VideoSorter(VideoSorterInterface):
    def __init__(self, source_dir:str, key_to_directory:dict[str,str]):
        self.key_to_directory = key_to_directory
        self.source_dir = source_dir
        last_moved = None

    def _quick_look(self, file_path):
        """Open the file in macOS Quick Look."""
        subprocess.run(['qlmanage', '-p', file_path], check=False)

    def _move_file(self, src, dest_dir):
        """Move file to destination directory, handling file name conflicts, and retain original metadata."""
        base_name = os.path.basename(src)
        dest = os.path.join(dest_dir, base_name)
        
        # Handle file name conflicts by appending a number if the file already exists
        if os.path.exists(dest):
            print(f"=====SAME FILE EXISTS {dest}======")
            file_name, file_extension = os.path.splitext(base_name)
            counter = 1
            # Create a new name until a unique one is found
            while os.path.exists(dest):
                new_name = f"{file_name}_{counter}{file_extension}"
                dest = os.path.join(dest_dir, new_name)
                counter += 1

        # Move the file to the destination
        shutil.move(src, dest)
        
        # Copy original metadata (creation, modification dates)
        creation_time = os.path.getctime(dest)
        modification_time = os.path.getmtime(dest)
        
        # Set original metadata back
        os.utime(dest, (creation_time, modification_time))
        
        return dest


    def _undo_move(self):
        """Undo the last file move."""
        global last_moved
        if last_moved:
            moved_file, original_location = last_moved
            shutil.move(moved_file, original_location)
            last_moved = None
            print(f"Moved {os.path.basename(moved_file)} back to {original_location}.")
        else:
            print("No file move to undo.")

    def _print_key_to_directory(self):
        """Print the key to directory mapping."""
        print("Current key to directory mappings:")
        for key, directory in self.key_to_directory.items():
            print(f"  {key}: {directory}")

        print("  u: Undo last move")
        print("  q: Quit")

    def sort_directory(self):
        """Process each .mp4 file in the directory."""
        global last_moved

        self._print_key_to_directory()
        
        mp4_files = sorted([f for f in Path(self.source_dir).glob("*.mp4") if not f.name.startswith("._")])

        if not mp4_files:
            print("No .mp4 files found in the directory.")
            return
        

        for mp4_file in tqdm(mp4_files):
            mp4_file = str(mp4_file)
            print(f"Opening {mp4_file} in Quick Look...")

            # Open in Quick Look
            self._quick_look(mp4_file)

            user_input = input("Your choice: ").strip().lower()

            if user_input in self.key_to_directory:
                dest_dir = self.key_to_directory[user_input]
                moved_path = self._move_file(mp4_file, dest_dir)
                last_moved = (moved_path, mp4_file)
                print(f"Moved {mp4_file} to {dest_dir}.")
            elif user_input == 'u':
                self._undo_move()
            elif user_input == 'q':
                print("Exiting...")
                break
            else:
                print("skipping")
                continue
