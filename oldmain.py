import os
from sys import argv
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import types
import functions.schemas as schemas
from functions.call_function import call_function

def main():
    args = argv[1:]
    verbose = len(args) > 1 and args[1] == "--verbose"
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    model_name = 'gemini-2.0-flash-001'

    if not args:
        print("AI code assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I profit?"')
        return 1

    available_functions = types.Tool(
            function_declarations=[
                schemas.schema_get_files_info,
                schemas.schema_get_file_content,
                schemas.schema_run_python_file,
                schemas.schema_write_file
                ]
            )

    my_prompt = argv[1]
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Configure the API
    genai.configure(api_key=api_key)
    
    # Create the model
    model = genai.GenerativeModel(model_name, system_instruction=system_prompt)

    # Generate content
    response = model.generate_content(
        my_prompt,
        tools=[available_functions]
    )

    if verbose:
        print(f"User prompt: {my_prompt}")
    
    # Look for function calls in the response parts
    for part in response.parts:
        if hasattr(part, 'function_call') and part.function_call.name:
            function_call = part.function_call
            # Convert the args to a dictionary for readable display
            args_dict = dict(function_call.args)
            #print(f'Calling function: {function_call.name}({args_dict})')
            call_func_response = call_function(function_call, verbose)
        
            if hasattr(call_func_response.parts[0].function_response, 'response'):
                if verbose:
                    print(f"-> {call_func_response.parts[0].function_response.response}")
            else:
                raise Exception("Error: no function calls found when expected.") 
        else:
            try:
                print(response.text)
            except ValueError:
                print("Could not extract text from response")


    if verbose and hasattr(response, 'usage_metadata'):
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
