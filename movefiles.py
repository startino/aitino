import os
import shutil

def move_files_out(directory):
    # Walk through all directories in the given directory
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            # Construct full file path
            file_path = os.path.join(dirpath, filename)
            # Construct destination path
            destination_path = os.path.join(directory, filename)
            # Move file to the parent directory
            shutil.move(file_path, destination_path)

# Call the function with the desired directory path
move_files_out(r'C:\Users\antop\Documents\flowt\pixar-characters')