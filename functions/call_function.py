import os
from google.genai import types
from functions.run_python import run_python_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file

function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
        }

def call_function(function_call_part, verbose=False):

    def create_response(name, response):
        return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name= name,
                        response=response,
                    )
                ],
            )

    func_name = function_call_part.name
    if not func_name:
        print(f"Error: Function has no name.")
        response= {"error": f"Function has no name."}
        return create_response("unknown", response)

    func_args = function_call_part.args or {}

    if not verbose:
        print(f' - Calling function: {func_name}')
    else:
        print(f"Calling function: {func_name}({func_args})")

    func_args["working_directory"] = "./calculator"

    if func_name in function_map:
        function_to_call = function_map[func_name]
        try:
            response = {"result": function_to_call(**func_args)}
        except Exception as e:
            response = {"error": f"Error calling {func_name}: {str(e)}"}
    else:
        response = {"error": f'Unknown function {func_name}'}

    return create_response(func_name, response)   
