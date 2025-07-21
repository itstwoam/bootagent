from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

search_dir = "calculator"
#search_type = [".", "pkg", "/bin", "../"]
#search_type = ["main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]#for 
#search_type = ["lorem.txt"] #for getting contents
#search_type = ["lorem.txt", "pkg/morelorem.txt", "/tmp/temp.txt"]#Write testing.
search_type = ["main.py", "main.py", "tests.py","../main.py", "nonexistent.py"]#run testing
#search_content = ["wait, this isn't lorem ipsum", "lorem ipsum dolor sit amet", "this should not be allowed"]
search_content = [[], ["3 + 5"],[], [],[]]

def run_tests(search_dir, search_type, search_content):
    for i in range(len(search_type)):
        contents = run_python_file(search_dir, search_type[i], search_content[i])
        print(contents)


    
run_tests(search_dir, search_type, search_content)
