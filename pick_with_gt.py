"""
This script pick all files from folder A to destination folder, if they have corresponding ground truth file from folder B.
And copy the ground truth files to another destination folder, if there are corresponding file in A

Example:
python3 pick_with_gt.py \
    --src_path=<src path> \
    --gt_path=<gt path> \
    --des_path=<des path> \
    --des_gt_path=<des gt path> \
    --remove_gt_tail=<delimiter
"""
import os
from pathlib import Path
import shutil
import argparse


def main(source_folder: str, gt_folder: str, destination_folder: str, des_gt_folder: str, remove_gt_tail: str):

    os.makedirs(destination_folder, exist_ok=True)
    os.makedirs(des_gt_folder, exist_ok=True)

    # Get a list of all PDF files in the source folder
    files = os.listdir(source_folder)
    files_dict = { str(Path(x).with_suffix("")) : x for x in files }
    # get a list of all ground truth files in gt folder
    gt_files = os.listdir(gt_folder)
    # e.g. { "A1234": "A1234-5.pdf" }
    gt_dict = {}
    for orig_gt in gt_files:
        # remove extension
        x = Path(orig_gt).with_suffix("")
        # if provided, remove the last section of filename by delimiter.
        # e.g. A12312-2 -> A12312
        if remove_gt_tail:
            split_x = str(x).split(remove_gt_tail)
            if len(split_x) > 1:
                split_x = split_x[:-1]
            x = remove_gt_tail.join(split_x)
        # only add if not existed
        if x not in gt_dict:
            gt_dict[x] = orig_gt

    # Copy the specified number of PDF files to the destination folder
    copied_files = []
    copied_gt_files = []
    for gt_name, gt_raw_path in gt_dict.items():
        # check if this file exists in src folder
        if gt_name in files_dict:
            print(f"\rChecking {len(copied_files)}/{len(gt_files)} ...", end="")
            # prepare full path
            source_file = os.path.join(source_folder, files_dict[gt_name])
            destination_file = os.path.join(destination_folder, files_dict[gt_name])
            source_gt_file = os.path.join(gt_folder, gt_raw_path)
            destination_gt_file = os.path.join(des_gt_folder, gt_raw_path)
            # copy this file to destination
            shutil.copy2(source_file, destination_file)
            copied_files.append(files_dict[gt_name])
            shutil.copy2(source_gt_file, destination_gt_file)
            copied_gt_files.append(gt_raw_path)
    print("")
    return copied_files, copied_gt_files



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Randomly copy PDF files from a source folder to a destination folder')
    parser.add_argument('--src_path', type=str, help='Path to the source folder')
    parser.add_argument('--gt_path', type=str, help='Path to the groundtruth folder')
    parser.add_argument('--des_path', type=str, help='Path to the destination folder')
    parser.add_argument('--des_gt_path', type=str, help='Path to the gt destination folder')
    parser.add_argument('--remove_gt_tail', type=str, help='If provided, each of the gt file name is splitted by given delimiter \
                        and remove the last portion.')
    args = parser.parse_args()

    copied, copied_gt = main(args.src_path, args.gt_path, args.des_path, args.des_gt_path, args.remove_gt_tail)
    print("")
    print("Files copied : ")
    print("")
    print(copied)
    print("")
    print("GT Files copied : ")
    print("")
    print(copied_gt)
    print("")
    print(f"Total {len(copied)} files.")

