import os
import openai
from dotenv import load_dotenv

load_dotenv()


def get_new_message(context, model_version, new_message):
    """
    Generates a response from the OpenAI API based on the provided context and new message.

    Parameters:
        context (list): A list of dictionaries representing the conversation history.
        model_version (str): The model version to use (e.g., 'gpt-4', 'o1-preview').
        new_message (str): The latest message input from the user.

    Returns:
        str: The generated response from the OpenAI API.
    """

    openai_api_key = os.getenv("OPEN_AI_TOKEN")
    print(openai_api_key)
    if not openai_api_key:
        raise ValueError("OPEN_AI_TOKEN environment variable not found.")
    openai.api_key = openai_api_key

    messages = context + [{"role": "user", "content": new_message}]

    try:
        response = openai.ChatCompletion.create(
            model=model_version,
            messages=messages
        )
        assistant_reply = response['choices'][0]['message']['content']
        return assistant_reply.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    context = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, who won the World Series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    ]
    model_version = "gpt-3.5-turbo"
    new_message = "Who was the MVP of that series?"
    response = get_new_message(context, model_version, new_message)
    print(response)
