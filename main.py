import os
from sys import argv
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    args = argv[1:]
    verbose = len(args) > 1 and args[1] == "--verbose"

    if not args:
        print("AI code assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I profit?"')
        return 1

    my_prompt = argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=my_prompt)]),]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
            model = 'gemini-2.0-flash-001',
            contents=messages,
            )

    if verbose:
        print(f"User prompt: {my_prompt}")
    print(response.text)
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
