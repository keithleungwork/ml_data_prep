"""
This script randomly draw N files from src_path folder and copy to the des_path folder.

Example:
python3 sampling.py \
    --src_path=<src> \
    --des_path=<des> \
    --num=400
"""
import os
import random
import shutil
import argparse


def main( source_folder: str, destination_folder: str, num_files_to_copy: int ):

    os.makedirs(destination_folder, exist_ok=True)

    # Get a list of all PDF files in the source folder
    files = os.listdir(source_folder)

    # Shuffle the list of PDF files
    random.shuffle(files)

    # Copy the specified number of PDF files to the destination folder
    copied_files = []
    for file in files[:num_files_to_copy]:
        source_file = os.path.join(source_folder, file)
        destination_file = os.path.join(destination_folder, file)
        shutil.copy2(source_file, destination_file)
        copied_files.append(file)

    return copied_files



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Randomly copy PDF files from a source folder to a destination folder')
    parser.add_argument('--src_path', type=str, help='Path to the source folder')
    parser.add_argument('--des_path', type=str, help='Path to the destination folder')
    parser.add_argument('--num', type=int, help='Number of files to copy')
    args = parser.parse_args()

    main(args.src_path, args.des_path, args.num)
