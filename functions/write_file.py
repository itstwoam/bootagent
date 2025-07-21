import os
from functions.check_border import check_border

def write_file(working_directory, file_path, content):
    if check_border(working_directory, file_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory.'
    file_path = os.path.join(working_directory, file_path)
    try:
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except:
        return f"Error: exception in functions/write_file.py"
