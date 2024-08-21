import os
import shutil
import hashlib
import csv
import logging
from tqdm import tqdm

def calculate_md5(file_path):
    """
    Calculates the MD5 checksum of a file.

    Args:
        file_path (str): The path to the file to be checksummed.

    Returns:
        str: The MD5 checksum of the file as a hexadecimal string.
             Returns None if an error occurs.
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

def copy_files_from_path(path, target_dir, csv_writer):
    """
    Copies .txt and .log files from a specified path to the target directory and logs the file metadata.

    Args:
        path (str): The source directory to search for files.
        target_dir (str): The destination directory where files will be copied.
        csv_writer (csv.writer): A CSV writer object to log file metadata.

    Returns:
        int: The number of files copied.
    """
    files_copied = 0
    
    if not os.path.exists(path):
        logging.warning(f"Path not found: {path}")
        print(f"Path not found: {path}")
        return files_copied
    
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.txt') or file_name.endswith('.log'):
                source_file = os.path.join(root, file_name)
                rel_path = os.path.relpath(source_file, path)
                target_file = os.path.join(target_dir, rel_path)

                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                shutil.copy2(source_file, target_file)

                creation_date = os.path.getctime(source_file)
                last_access_date = os.path.getatime(source_file)
                md5_checksum = calculate_md5(source_file)

                csv_writer.writerow([file_name, source_file, creation_date, last_access_date, md5_checksum])

                files_copied += 1
                logging.info(f"Copied {source_file} to {target_file}")
                print(f"Copied {source_file} to {target_file}")
    
    return files_copied

def copy_teamviewer_files(target_dir):
    """
    Copies TeamViewer log and text files from the common directory to a specified target directory,
    and logs metadata to a CSV file.

    Args:
        target_dir (str): The directory where the files will be copied.
    """
    try:
        # Define the path to search for TeamViewer files
        paths_to_search = [
            r"C:\Program Files (x86)\TeamViewer"
        ]
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        csv_file_path = os.path.join(target_dir, "teamviewer_files.csv")
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["File Name", "File Path", "Creation Date", "Last Access Date", "MD5 Checksum"])
        
            files_copied = 0
        
            for base_path in paths_to_search:
                files_copied += copy_files_from_path(base_path, target_dir, csv_writer)
        
        if files_copied == 0:
            logging.warning("No TeamViewer text files or log files found.")
            print("No TeamViewer text files or log files found.")
        else:
            logging.info(f"All TeamViewer files have been copied successfully. Total files copied: {files_copied}")
            print(f"All TeamViewer files have been copied successfully. Total files copied: {files_copied}")
    except Exception as e:
        logging.error(f"An error occurred while copying TeamViewer files: {e}")
        print(f"An error occurred while copying TeamViewer files: {e}")

if __name__ == "__main__":
    logging.basicConfig(filename='logs/teamviewer_extractor.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    target_directory = "TeamViewer_export"
    copy_teamviewer_files(target_directory)
    input("Press any key to close the window...")
