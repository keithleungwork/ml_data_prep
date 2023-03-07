"""
Convert ALL PDF files in a folder to images

Example :
python3 cuspdf2image.py --src_path=test/pdf/ --out_path=test/img
"""
import argparse
from pathlib import Path
from pdf2image import convert_from_path
import os



def pdf_to_image(file_path: Path, output_folder: Path, dpi: int):
    # pdf2image method
    convert_from_path(
        file_path,
        output_folder=output_folder,
        last_page=1,
        dpi=dpi,
        fmt="png",
        grayscale=True
    )

def main(dir_path: str, out_dir: str, dpi: int = 400) -> None:
    # create output folder if not existed
    os.makedirs(os.path.dirname(out_dir), exist_ok=True)
    # For display usage
    file_length = len(os.listdir(dir_path))
    count = 0
    for filename in os.listdir(dir_path):
        # Only deal with PDF
        if filename.endswith('.pdf'):
            count+=1
            try:
                print(f"\rProcessing {count}/{file_length} ...", end="")
                pdf_to_image(Path(dir_path).joinpath(filename), Path(out_dir), dpi=dpi)
            except Exception as e:
                print("")
                print("error: ", filename)
                print(e)
                print("")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='pdf to image')
    parser.add_argument('--src_path', type=str, help='path to the pdf directory', required=True)
    parser.add_argument('--out_path', type=str, help='path to the output directory', required=True)

    args = parser.parse_args()

    main(args.src_path, args.out_path)
