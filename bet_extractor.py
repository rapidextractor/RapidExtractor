import os 
import shutil
import hashlib
import csv
import logging
from tqdm import tqdm

def calculate_md5(file_path):
    """
    Calculates MD5 checksum of a file.

    Args:
        file_path (str): The path to the file that needs to be checksummed.

    Returns:
        str: The MD5 checksum of the file as a hex-string.
             Returns None if an error occurs during calculation.
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

def copy_directory_with_metadata(src, dst, csv_writer):
    """
    Recursively copies files from the source directory to the destination directory,
    preserving file metadata and logging the details into a CSV file.

    Args:
        src (str): source directory path.
        dst (str): destination directory path.
        csv_writer (csv.writer): CSV writer object for logging file metadata.
    """
    if not os.path.exists(dst):
        os.makedirs(dst)
    
    items = os.listdir(src)
    for item in tqdm(items, desc="Copying files", unit="file"):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        if os.path.isdir(s):
            copy_directory_with_metadata(s, d, csv_writer)
        else:
            shutil.copy2(s, d)

            creation_date = os.path.getctime(s)
            last_access_date = os.path.getatime(s)
            md5_checksum = calculate_md5(s)

            csv_writer.writerow([os.path.basename(s), s, creation_date, last_access_date, md5_checksum])

def copy_bet_files(target_dir):
    """
    Copies BET log files from default source directory (C:\\BET\\Logs) to the target directory (usually on the investigators drive),
    and logs metadata to a CSV file.

    Args:
        target_dir (str): The directory where the log files will be copied to.
    """
    try:
        logs_src = r"C:\\BET\\Logs"  
        logs_dst = os.path.join(target_dir, 'Logs')

        # Create BET_export directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        csv_file_path = os.path.join(target_dir, "bet_files.csv")
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["File Name", "File Path", "Creation Date", "Last Access Date", "MD5 Checksum"])

            copy_directory_with_metadata(logs_src, logs_dst, csv_writer)

        print("BET logs have been copied successfully.")
    except Exception as e:
        print(f"An error occurred while copying BET logs: {e}")
        logging.error(f"Error copying BET logs: {e}")

if __name__ == "__main__":
    logging.basicConfig(filename='logs/bet_extractor.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    target_directory = "bet_export"
    copy_bet_files(target_directory)
    input("Press any key to close the window...")
