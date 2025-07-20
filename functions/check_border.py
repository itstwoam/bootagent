import os

def check_border(working_directory, target_path="."):
    base_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(base_dir, target_path))
    if os.path.commonpath([base_dir]) != os.path.commonpath([base_dir, full_path]):
        return True
    return False
