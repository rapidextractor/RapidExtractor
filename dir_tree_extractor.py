import os
import time  
from tqdm import tqdm
import logging

def generate_dir_tree(start_path, output_file):
    """
    Generates a directory tree starting from the given path and writes it to the specified output file.

    Args:
    start_path (str): The root directory path to start generating the tree.
    output_file (str): The file where the directory tree will be saved.
    """
    def tree(dir_path, prefix=''):
        """
        A helper function to recursively generate the directory tree structure.

        Args:
        dir_path (str): The current directory path.
        prefix (str): The prefix for the current level in the directory tree.
        """
        try:
            contents = sorted(os.listdir(dir_path))
        except PermissionError:
            contents = []
            f.write(prefix + '    [Permission Denied]\n')
            progress_bar.update(1)
            return
        except FileNotFoundError:
            contents = []
            f.write(prefix + '    [File Not Found]\n')
            progress_bar.update(1)
            return

        pointers = [contents.index(item) == len(contents) - 1 for item in contents]

        for pointer, path in zip(pointers, contents):
            full_path = os.path.join(dir_path, path)
            connector = '└── ' if pointer else '├── '
            line = prefix + connector + path
            try:
                f.write(line + '\n')
                if os.path.isdir(full_path):
                    extension = '    ' if pointer else '│   '
                    tree(full_path, prefix + extension)
                progress_bar.update(1)
            except PermissionError:
                f.write(prefix + '    [Permission Denied]\n')
                progress_bar.update(1)
            except FileNotFoundError:
                f.write(prefix + '    [File Not Found]\n')
                progress_bar.update(1)

    logging.info(f"Generating directory tree starting from {start_path}...")
    print(f"Generating directory tree starting from {start_path}...")

    try:
        total_entries = sum([len(files) + len(dirs) for _, dirs, files in os.walk(start_path)])
        with open(output_file, 'w', encoding='utf-8') as f, tqdm(total=total_entries, desc="Generating Directory Tree") as progress_bar:
            tree(start_path)
        logging.info(f"Directory tree has been saved to {output_file}")
        print(f"Directory tree has been saved to {output_file}")
    except Exception as e:
        logging.error(f"An error occurred while generating the directory tree: {e}")
        print(f"An error occurred while generating the directory tree: {e}")

def extract_dir_tree(target_dir):
    """
    Extracts the directory tree starting from the root directory and saves it to the target directory.

    Args:
    target_dir (str): The directory where the output file will be saved.
    """
    start_time = time.time()
    root_dir = "C:\\"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    output_file = os.path.join(target_dir, 'dir_tree.txt')
    logging.info(f"Saving directory tree to {output_file}...")
    print(f"Saving directory tree to {output_file}...")
    generate_dir_tree(root_dir, output_file)
    end_time = time.time()
    logging.info(f"Directory tree successfully saved to {output_file}. Extraction took {end_time - start_time:.2f} seconds.")
    print(f"Directory tree successfully saved to {output_file}")
    print(f"Extraction took {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    # Configure logging to record debug information in a log file.
    logging.basicConfig(filename='logs/dir_tree_extractor.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    target_directory = "DirTree_export"
    extract_dir_tree(target_directory)
    input("Press any key to close the window...")
