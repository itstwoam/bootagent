import os
from functions.check_border import check_border

def get_files_info(working_directory, directory="."):
    if check_border(working_directory, directory):
        return 'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    base_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(base_dir, directory))
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    file_list = []
    scanned = os.listdir(full_path)
    for f in scanned:
        file_path = os.path.join(full_path, f)
        file_list.append(f'- {file_path}: file_size={os.path.getsize(file_path)} bytes, is_dir={not os.path.isfile(file_path)}')
    return file_list
