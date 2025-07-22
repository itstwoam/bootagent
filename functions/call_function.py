import os
import google.generativeai as genai
from google.generativeai import types
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

    function_args = function_call_part.args
    if not verbose:
        print(f' - Calling function: {function_call_part.name}')
    else:
        print(f"Calling function: {function_call_part.name}({function_args})")

    function_args["working_directory"] = "./calculator"

    return_content = {}

    if function_call_part.name in function_map:
        function_to_call = function_map[function_call_part.name]

        result = function_to_call(**function_args)
        return_content["result"] = result
    else:
        return_content["error"] = f'Unknown function {function_call_part.name}'

    return {
        "role":"tool",
        "parts":[
            {
                "function_response":{
                "name": function_call_part.name,
                "response": return_content
                }
            }
        ]
    }
