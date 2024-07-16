import argparse
from pathlib import Path

def rename_files_in_folder(input_folder, base_name, output_folder=None):
    """
    Renames all files in a given folder with a specified base name and incremental suffix.

    Parameters:
    input_folder (str): The path to the folder containing files to rename.
    base_name (str): The base name for the renamed files.
    output_folder (str, optional): The path to the folder where renamed files will be saved. If not provided, the files will be renamed in the input folder.

    Returns:
    None
    """

    input_folder = Path(input_folder)
    if not input_folder.is_dir():
        print(f"The provided path {input_folder} is not a directory.")
        return

    if output_folder:
        output_folder = Path(output_folder)
        if not output_folder.exists():
            output_folder.mkdir(parents=True)
    else:
        output_folder = input_folder

    files = sorted(input_folder.iterdir())
    suffix = 1

    for file in files:
        if file.is_file():
            new_name = f"{base_name}_{suffix}{file.suffix}"
            new_file_path = output_folder / new_name
            file.rename(new_file_path)
            suffix += 1

def main():
    parser = argparse.ArgumentParser(description='Rename files in a folder with a given base name and incremental suffix.')
    parser.add_argument('input_folder', type=str, help='Path to the folder containing files to rename.')
    parser.add_argument('base_name', type=str, help='Base name for the renamed files.')
    parser.add_argument('--output_folder', type=str, help='Path to the folder where renamed files will be saved.')

    args = parser.parse_args()
    rename_files_in_folder(args.input_folder, args.base_name, args.output_folder)

if __name__ == '__main__':
    main()
