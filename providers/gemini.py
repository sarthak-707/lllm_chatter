from os     import getenv
from google import genai
from dotenv import load_dotenv

load_dotenv()

"""Load API key"""
GEMINI_API_KEY = getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise EnvironmentError("API key not found.")
client = genai.Client(api_key=GEMINI_API_KEY)


def chat(current_model:str):
    """ Starts a new chat
        current_model = The model that will be used for chat.
    """
    response = client.chats.create(model= current_model)
    total_token_count = 0
    last_chunk = None

    while True:
        message =input("\n> ")
        if message.lower() == "exit":
            yield "Exited successfully.\n"
            break

        try:
            result = response.send_message_stream(message)
            for chunks in result:
                if chunks.text:
                    yield chunks.text
                last_chunk = chunks

            metadata = getattr(last_chunk, "usage_metadata", None)

            total_token_count += getattr(metadata, "total_token_count", 0)
            output_tokens = getattr(metadata, "candidates_token_count", -1)
            input_tokens = getattr(metadata, "prompt_token_count", -1)

            usage_data = f"\nTotal Tokens : {total_token_count}\nOutput: {output_tokens} Input : {input_tokens}\n"
            yield usage_data

        except Exception as e:
            yield f"Error: {e}\n"

for chunk in chat("gemini-2.0-flash-lite"):
    print(chunk, end="", flush=True)
