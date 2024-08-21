import os               # Provides functions for interacting with the OS file paths.
import shutil           # Offers higher-level file operations, such as copying, moving, and archiving files and directories.
import hashlib           # Provides hashing algorithms (for RapidExtractor MD5 is used).
import csv              # Enables reading from and writing to CSV files (used to store metadata and hashvalues).
import logging          # Provides a framework for logging messages from applications, useful for error handling (debugging) and tracking events.
from tqdm import tqdm   # Adds a progress bar to loops and iterable operations, enhancing user feedback during long-running processes.

def calculate_md5(file_path):
    """
    Calculates the MD5 checksum of a file.

    Args:
        file_path (str): the path to the file that needs to be checksummed.

    Returns:
        str: MD5 checksum of the file as a hex-string.
             Returns None if an error occurs during calculation.
    """
    hash_md5 = hashlib.md5()  # Create an MD5 hash object
    try:
        with open(file_path, "rb") as f:
            # Read the file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()  # Return the hexadecimal MD5 checksum
    except Exception as e:
        logging.error(f"An error occurred while calculating MD5 for {file_path}: {e}")
        return None

def copy_file_with_metadata(src, dst, csv_writer):
    """
    Copies a file from the source path to the destination path,
    preserving file metadata and logging the details ino a CSV file.

    Args:
        src (str): The source file path.
        dst (str): The destination file path.
        csv_writer (csv.writer): A CSV writer object for logging file metadata.
    """
    # Ensure the destination directory exists
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    
    # Copy the file while preserving metadata
    shutil.copy2(src, dst)

    # Get file metadata
    creation_date = os.path.getctime(src)
    last_access_date = os.path.getatime(src)
    md5_checksum = calculate_md5(src)

    # Write the metadata to the CSV file
    csv_writer.writerow([os.path.basename(src), src, creation_date, last_access_date, md5_checksum])

def extract_edge_history(target_dir, csv_writer):
    """
    Extracts Microsoft Edge browsing history and copies it to the target directory,
    logging file metadata to the CSV file.

    Args:
        target_dir (str): The directory where the history file will be copied.
        csv_writer (csv.writer): A CSV writer object for logging file metadata.
    """
    try:
        edge_history_path = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History')
        if os.path.exists(edge_history_path):
            edge_target_dir = os.path.join(target_dir, 'Edge')
            copy_file_with_metadata(edge_history_path, os.path.join(edge_target_dir, 'History'), csv_writer)
            print(f"Copied Edge history to {edge_target_dir}")
        else:
            logging.warning("Edge history file not found. Maybe it is not installed?")
    except Exception as e:
        logging.error(f"Error extracting Edge history: {e}")

def extract_firefox_history(target_dir, csv_writer):
    """
    Extracts Mozilla Firefox browsing history and copies it to the target directory,
    logging file metadata to the CSV file.

    Args:
        target_dir (str): The directory where the history files will be copied.
        csv_writer (csv.writer): A CSV writer object for logging file metadata.
    """
    try:
        firefox_profile_dir = os.path.expandvars(r'%APPDATA%\Mozilla\Firefox\Profiles')
        if os.path.exists(firefox_profile_dir):
            for profile in os.listdir(firefox_profile_dir):
                history_path = os.path.join(firefox_profile_dir, profile, 'places.sqlite')
                if os.path.exists(history_path):
                    firefox_target_dir = os.path.join(target_dir, 'Firefox', profile)
                    copy_file_with_metadata(history_path, os.path.join(firefox_target_dir, 'places.sqlite'), csv_writer)
                    print(f"Copied Firefox history for profile {profile} to {firefox_target_dir}")
        else:
            logging.warning("Firefox profiles directory not found. Maybe it is not installed?")
    except Exception as e:
        logging.error(f"Error extracting Firefox history: {e}")

def extract_chrome_history(target_dir, csv_writer):
    """
    Extracts Google Chrome browsing history and copies it to the target directory,
    logging file metadata to the CSV file.

    Args:
        target_dir (str): The directory where the history file will be copied.
        csv_writer (csv.writer): A CSV writer object for logging file metadata.
    """
    try:
        chrome_profile_dir = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default')
        if os.path.exists(chrome_profile_dir):
            chrome_history_path = os.path.join(chrome_profile_dir, 'History')
            if os.path.exists(chrome_history_path):
                chrome_target_dir = os.path.join(target_dir, 'Chrome')
                copy_file_with_metadata(chrome_history_path, os.path.join(chrome_target_dir, 'History'), csv_writer)
                print(f"Copied Chrome history to {chrome_target_dir}")
        else:
            logging.warning("Chrome profile directory not found. Maybe it is not installed?")
    except Exception as e:
        logging.error(f"Error extracting Chrome history: {e}")

def extract_browser_histories(target_dir):
    """
    Extracts browsing histories from Edge, Firefox, and Chrome, and copies them to the target directory,
    logging metadata to a CSV file.

    Args:
        target_dir (str): The directory where the history files will be copied.
    """
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        csv_file_path = os.path.join(target_dir, "browser_history.csv")
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["File Name", "File Path", "Creation Date", "Last Access Date", "MD5 Checksum"])

            extract_edge_history(target_dir, csv_writer)
            extract_firefox_history(target_dir, csv_writer)
            extract_chrome_history(target_dir, csv_writer)

        print("Browser histories have been copied successfully.")
    except Exception as e:
        print(f"An error occurred while extracting browser histories: {e}")
        logging.error(f"Error extracting browser histories: {e}")

if __name__ == "__main__":
    # Configure logging to record debug information in a log file
    logging.basicConfig(filename='logs/browser_history_extractor.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    
    # Define the target directory for exporting browser histories
    target_directory = "BrowserHistory_export"
    
    # Execute the extraction of browser histories and metadata logging
    extract_browser_histories(target_directory)
    
    # Wait for user input before closing the script
    input("Press any key to close the window...")
