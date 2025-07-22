import os
from sys import argv
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import types
import functions.schemas as schemas
from functions.call_function import call_function

available_functions = types.Tool(
        function_declarations=[
        schemas.schema_get_files_info,
        schemas.schema_get_file_content,
        schemas.schema_run_python_file,
        schemas.schema_write_file
        ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

If any arguments for function calls are desired by me they will be stated.  If none are stated then you may add them if required by the task, no need to ask for clarification.
"""

model_name = 'gemini-2.0-flash-001'

def main():
    args = argv[1:]
    verbose = len(args) > 1 and args[1] == "--verbose"
    
    
    if not args:
        print("AI code assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I profit?"')
        return 1

    my_prompt = argv[1]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Configure the API
    genai.configure(api_key=api_key)
    
    # Create the model
    model = genai.GenerativeModel(model_name, system_instruction=system_prompt)

    iterations = 1

    # Generate content
    model_response = gen_content(model,
            my_prompt,
            verbose
    )


    while iterations < 20:
        iterations += 1            

        #Check response for function call.

        #If not then set iterations to 21
        if not model_response.function_calls:





def gen_content(model, content, verbose):
    model_response = model.generate_content(
        content,
        tools=[available_functions]
    )

    if verbose:
        print(f"User prompt: {content}")
    
    # Look for function calls in the response parts
    for part in model_response.parts:
        if hasattr(part, 'function_call') and part.function_call.name:
            function_call = part.function_call
            # Convert the args to a dictionary for readable display
            args_dict = dict(function_call.args)
            #print(f'Calling function: {function_call.name}({args_dict})')
            call_func_response = call_function(function_call, verbose)
        
            if 'function_response' in call_func_response["parts"][0] and 'response' in call_func_response["parts"][0]["function_response"]:
                if verbose:
                    print(f"-> {call_func_response['parts'][0]['function_response']['response']}")
            else:
                raise Exception("Error: no function calls found when expected.") 
        else:
            try:
                print(model_response.text)
            except ValueError:
                print("Could not extract text from response")


    if verbose and hasattr(model_response, 'usage_metadata'):
        print(f"Prompt tokens: {model_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {model_response.usage_metadata.candidates_token_count}")





#
if __name__ == "__main__":
    main()
