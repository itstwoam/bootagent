from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

search_dir = "calculator"
#search_type = [".", "pkg", "/bin", "../"]
search_type = ["main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]
#search_type = ["lorem.txt"]

def search_directoryies(search_dir, search_type):
    for i in range(len(search_type)):
        files = get_files_info(search_dir, search_type[i])
        print(f"Result for {search_type[i]} directory:")
        if "Error:" not in files:
            for f in files:
                print("   "+f)
        else:
            print(f'   Error: Cannot list "{search_type[i]}" as it is outside the permitted working directory')

def search_content(search_dir, search_type):
    for i in range(len(search_type)):
        contents = get_file_content(search_dir, search_type[i])
        print(contents)

search_content(search_dir, search_type)
