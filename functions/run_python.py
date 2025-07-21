import os
import subprocess
import sys
from functions.check_border import check_border

def run_python_file(working_directory, file_path, args=[]):
    if check_border(working_directory, file_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    full_file_path = os.path.join(working_directory, file_path)

    if not os.path.exists(full_file_path):
        return f'Error: File "{file_path}" not found.'

    if not full_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed = subprocess.run([sys.executable, full_file_path] + args, timeout=30, capture_output=True, text=True)
        stdo = f'STDOUT: {completed.stdout}'
        stde = f'STDERR: {completed.stderr}'
        code = completed.returncode
        if len(completed.stdout) > 0 or len(completed.stderr) > 0:
            result = "\n".join([stdo, stde])
        else:
            result = "No output produced."
        if completed.returncode != 0:
            result = "\n".join([result, f'Process exited with code: {code}'])
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"
