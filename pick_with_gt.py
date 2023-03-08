"""
This script pick all files from folder A to destination folder, if they have corresponding ground truth file from folder B.

Example:
python3 pick_with_gt.py \
    --src_path=<src path> \
    --gt_path=<gt path> \
    --des_path=<des path>
"""
import os
from pathlib import Path
import shutil
import argparse


def main(source_folder: str, gt_folder: str, destination_folder: str):

    os.makedirs(destination_folder, exist_ok=True)

    # Get a list of all PDF files in the source folder
    files = os.listdir(source_folder)
    files_dict = { str(Path(x).with_suffix("")) : x for x in files }
    # get a list of all ground truth files in gt folder
    gt_files = os.listdir(gt_folder)
    for i, x in enumerate(gt_files):
        # remove extension
        x = Path(x).with_suffix("")
        gt_files[i] = "-".join(str(x).split("-")[:-1])
    gt_files = set(gt_files)

    # Copy the specified number of PDF files to the destination folder
    copied_files = []
    for gt_name in gt_files:
        # check if this file exists in src folder
        if gt_name in files_dict:
            print(f"\rChecking {len(copied_files)}/{len(gt_files)} ...", end="")
            # prepare full path
            source_file = os.path.join(source_folder, files_dict[gt_name])
            destination_file = os.path.join(destination_folder, files_dict[gt_name])
            # copy this file to destination
            shutil.copy2(source_file, destination_file)
            copied_files.append(files_dict[gt_name])
    print("")
    return copied_files



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Randomly copy PDF files from a source folder to a destination folder')
    parser.add_argument('--src_path', type=str, help='Path to the source folder')
    parser.add_argument('--gt_path', type=str, help='Path to the groundtruth folder')
    parser.add_argument('--des_path', type=str, help='Path to the destination folder')
    args = parser.parse_args()

    copied = main(args.src_path, args.gt_path, args.des_path)
    print("")
    print("Files copied : ")
    print("")
    print(copied)
    print("")
    print(f"Total {len(copied)} files.")

