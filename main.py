import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import Client, types
from functions.schemas import *
from functions.call_function import call_function

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan.  You can perform the following operations:
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

All paths you provide should be relative to the working directory.  You do not need to specify the working directory in your function calls as it is automatically injected for security reasons. If not directly told what parameters to use then you may use or create any arguments you feel are required to complete the task as instructed, no need to ask for clarification.

Unless otherwise stated any questions asked will be related to the calculator app main.py in the root directory.
Please use lists with short to medium line lengths when describing prcoesses when possible.
"""

available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
            ]
        )

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    model_name = "gemini-2.0-flash-001"

    if len(sys.argv) < 2 or sys.argv[1] == "--verbose":
        print("Error: No prompt given.")
        sys.exit(1)

    verbose = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose = True

    my_config = types.GenerateContentConfig(tools= [available_functions], system_instruction=system_prompt)

    my_prompt = sys.argv[1]

    if verbose:
        print(f'User prompt: {my_prompt}')

    messages = [
        types.Content(role="user", parts=[types.Part(text=my_prompt)])
        ]
    
    MAX_LOOP = 20
    iterations = 0

    while iterations < MAX_LOOP:
        iterations += 1

        try:
            final_response = generate_content(client, model_name, messages, my_config, verbose)
            if final_response:
                print("Final response: "+final_response)
                return 0
        except Exception as e:
            print(f"Exception in generate_content: {e}")

    print(f"Maximum iterations({MAX_LOOP}) reached, aborting.")
        
def generate_content(client, model, contents, config, verbose):    
    model_response = client.models.generate_content(
        model= model,
        contents=contents,
        config=config
        )

    if verbose:
        print(f'Promt tokens: {model_response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {model_response.usage_metadata.candidates_token_count}')

    for candidate in model_response.candidates:
        if candidate.content:
            contents.append(candidate.content)
    if not model_response.function_calls:
        return model_response.text

    function_responses = []
    if model_response.function_calls:
        for call in model_response.function_calls:
            call_response = call_function(call, verbose)
            if not call_response.parts[0].function_response.response:
                raise exception("Error no response in function response.")

            if verbose:
                print(f"-> {call_response.parts[0].function_response.response}")

            
            function_responses.append(call_response.parts[0])
        contents.append(types.Content(role="tool", parts=function_responses))


if __name__ == "__main__":
    main()
