import os
import glob
from PIL import Image
import re

def convert_to_webp(directory):
    # Find all image files in the given directory and its subdirectories
    for image_file in glob.glob(directory + '/**', recursive=True):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Open the image file, convert it to webp, and save it
            Image.open(image_file).save(image_file.rsplit('.', 1)[0] + '.webp')

def replace_in_code(directory):
    # Find all code files in the given directory and its subdirectories
    for code_file in glob.glob(directory + '/**', recursive=True):
        if code_file.endswith('.py'):  # or any other file types you want to process
            # Open the code file, read its contents
            with open(code_file, 'r') as file:
                contents = file.read()
            # Replace all occurrences of the image file names with the .webp extension
            contents = re.sub(r'(\.png|\.jpg|\.jpeg)', '.webp', contents, flags=re.IGNORECASE)
            # Write the modified contents back to the file
            with open(code_file, 'w') as file:
                file.write(contents)

# Call the functions with the desired directory paths
convert_to_webp('./static_1')
replace_in_code('./src_1')