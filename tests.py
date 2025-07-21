from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

search_dir = "calculator"
#search_type = [".", "pkg", "/bin", "../"]
#search_type = ["main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]#for 
#search_type = ["lorem.txt"] #for getting contents
search_type = ["lorem.txt", "pkg/morelorem.txt", "/tmp/temp.txt"]
search_content = ["wait, this isn't lorem ipsum", "lorem ipsum dolor sit amet", "this should not be allowed"]
def search_directoryies(search_dir, search_type):
    for i in range(len(search_type)):
        files = get_files_info(search_dir, search_type[i])
        print(f"Result for {search_type[i]} directory:")
        if "Error:" not in files:
            for f in files:
                print("   "+f)
        else:
            print(f'   Error: Cannot list "{search_type[i]}" as it is outside the permitted working directory')

def search_contents(search_dir, search_type):
    for i in range(len(search_type)):
        contents = get_file_content(search_dir, search_type[i])
        print(contents)

def write_tests(search_dir, search_type, search_content):
    for i in range(len(search_type)):
        status = write_file(search_dir, search_type[i], search_content[i])
        print(status)

write_tests(search_dir, search_type, search_content)
