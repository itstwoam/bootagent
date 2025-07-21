import os
import google.generativeai as genai
from google.generativeai import types
from functions.run_python import run_python_file

function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_files_content,
        "run_python_file": run_python_file,
        "write_file": write_file
        }

def call_function(function_call_part, verbose=False)
    output = f' - Calling function: {function_call_part.name}')
    argu = function_call_part.args
    if verbose:
        output = output + "(" + argsu + ")"

    argu["working_dir"] = "./calculator"


    return_content = {}

    if function_call_part.name in function_map:
        function_to_call = function_map[function_call_part.name]

        result = function_to_call(**argu)
        return_content["result"] = result
    else:
        return_content["error"] = f'Unknown function {function_call_part.name}'},
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response=return_content,
                )
            ],
        )
