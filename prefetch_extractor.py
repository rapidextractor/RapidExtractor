import os
import shutil
import hashlib
import csv
from tqdm import tqdm
import logging

def calculate_md5(file_path):
    """
    Calculates the MD5 checksum of a file.

    Args:
    file_path (str): The path to the file.

    Returns:
    str: The MD5 checksum of the file.
    """
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logging.error(f"An error occurred while calculating MD5 for {file_path}: {e}")
        return None

def copy_prefetch_files(target_dir):
    """
    Copies all Prefetch files from the Windows Prefetch directory (%RootDir%\\Windows\\Prefetch) to the specified target directory,
    and logs the details including file path, creation date, last access date, and MD5 checksum in a CSV file.

    Args:
    target_dir (str): The directory where the Prefetch files will be copied.
    """
    try:
        prefetch_dir = os.path.join(os.environ['WINDIR'], 'Prefetch')
        if not os.path.exists(prefetch_dir):
            logging.warning(f"Prefetch directory not found: {prefetch_dir}")
            print(f"Prefetch directory not found: {prefetch_dir}")
            return

        total_files = sum(len(files) for _, _, files in os.walk(prefetch_dir))
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        csv_file_path = os.path.join(target_dir, "prefetch_files.csv")
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["File Name", "File Path", "Creation Date", "Last Access Date", "MD5 Checksum"])

            with tqdm(total=total_files, desc="Copying Prefetch Files") as pbar:
                for root, dirs, files in os.walk(prefetch_dir):
                    for file_name in files:
                        source_file = os.path.join(root, file_name)
                        rel_path = os.path.relpath(source_file, os.path.dirname(prefetch_dir))
                        target_file = os.path.join(target_dir, 'Windows', rel_path)

                        os.makedirs(os.path.dirname(target_file), exist_ok=True)
                        shutil.copy2(source_file, target_file)

                        creation_date = os.path.getctime(source_file)
                        last_access_date = os.path.getatime(source_file)
                        md5_checksum = calculate_md5(source_file)

                        csv_writer.writerow([file_name, source_file, creation_date, last_access_date, md5_checksum])

                        pbar.update(1)

        logging.info("All prefetch files have been copied successfully, and details have been saved to CSV.")
        print("All prefetch files have been copied successfully, and details have been saved to CSV.")
    except Exception as e:
        logging.error(f"An error occurred while copying prefetch files: {e}")
        print(f"An error occurred while copying prefetch files: {e}")

if __name__ == "__main__":
    # Configure logging to record debug information in a log file.
    logging.basicConfig(filename='logs/prefetch_extractor.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    target_directory = "Prefetch_export"
    copy_prefetch_files(target_directory)
    input("Press any key to close the window...")
