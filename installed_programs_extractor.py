import os
from tqdm import tqdm

def copy_top_level_directories(src, dst):
    """
    Copies only the top-level directories from src to dst without copying any files or subdirectories.

    Args:
    src (str): Source directory.
    dst (str): Destination directory.
    """
    # Get the list of top-level directories in the source directory
    top_level_dirs = [name for name in os.listdir(src) if os.path.isdir(os.path.join(src, name))]

    for directory in tqdm(top_level_dirs, desc=f"Copying top-level directories from {src}"):
        # Create corresponding target directory
        target_dir = os.path.join(dst, directory)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)




def main():
    directories_to_copy = [
        r"C:\Program Files",
        r"C:\Program Files (x86)"
    ]
    target_directory = "CopiedStructure"

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    for directory in directories_to_copy:
        copy_top_level_directories(directory, target_directory)

    print(f"The top-level directories have been copied successfully to '{target_directory}'.")

if __name__ == "__main__":
    main()
