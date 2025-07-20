import os
from functions.check_border import check_border

def get_file_content(working_directory, file_path):
    if check_border(working_directory, file_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    base_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(base_dir, file_path))
    if os.path.isdir(full_path):
        return f'Error: File not found or is not a regular file:"{full_path}"'
    MAX_CHARS = 10000
    file_content_string = ""
    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except:
        file_content_string = f"Error: File '{full_path}' does not exist."
    return file_content_string
