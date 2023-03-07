"""
This script helps to randomly split files into train, test paths (or eval also)
The split size can be via exact file size OR split ratio

Example :
python3 split_data.py \
    --src_dir <src folder full path> \
    --train_dir <train folder full path> \
    --test_dir <test folder full path> \
    --eval_dir <eval folder full path> \
    <Split by exact file size>
    --test_size 1 \
    --eval_size 2
    <Split by ratio>
    --test_ratio 0.1 \
    --eval_ratio 0.2
"""
import os
import shutil
import argparse
from sklearn.model_selection import train_test_split


def main( input_dir: str, train_dir: str, test_dir: str, eval_dir: str, split_ratio: list):
    if split_ratio is None:
        return False
    # Create the train and test directories if they don't already exist
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    if eval_dir:
        os.makedirs(eval_dir, exist_ok=True)

    # Set the ratio of files to allocate to each directory
    test_size, eval_size = split_ratio

    # Get a list of all the files in the input directory
    files = os.listdir(input_dir)

    # Split the files into train, test and eval sets
    train_files, test_eval_files = train_test_split(files, test_size=test_size + eval_size)
    if eval_size > 0:
        test_files, eval_files = train_test_split(test_eval_files, test_size=eval_size/(test_size+eval_size))
    else:
        test_files, eval_files = test_eval_files, []

    # Copy the files into the appropriate directories
    for file in train_files:
        shutil.copy(os.path.join(input_dir, file), train_dir)
    for file in test_files:
        shutil.copy(os.path.join(input_dir, file), test_dir)
    if eval_dir:
        for file in eval_files:
            shutil.copy(os.path.join(input_dir, file), eval_dir)

    return train_files, test_files, eval_files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split a dataset into train and test sets')
    parser.add_argument('--src_dir', type=str, help='path to the dataset directory', required=True)
    parser.add_argument('--train_dir', type=str, help='path to the train directory', required=True)
    parser.add_argument('--test_dir', type=str, help='path to the test directory', required=True)
    parser.add_argument('--eval_dir', type=str, help='path to the eval directory', required=False)
    parser.add_argument('--test_size', type=int, help='size of test set')
    parser.add_argument('--eval_size', type=int, help='size of eval set', default=0)
    parser.add_argument('--test_ratio', type=float, help='ratio of test set')
    parser.add_argument('--eval_ratio', type=float, help='ratio of eval set', default=0)

    args = parser.parse_args()

    # Use exact file size if provided
    if args.test_size:
        split_ratio = [args.test_size, args.eval_size]
    else:
        split_ratio = [args.test_ratio, args.eval_ratio]

    train_files, test_files, eval_files = main(
        args.src_dir, args.train_dir, args.test_dir, args.eval_dir,
        split_ratio
    )

    print("train_files : ", len(train_files))
    print("test_files : ", len(test_files))
    print("eval_files : ", len(eval_files))
