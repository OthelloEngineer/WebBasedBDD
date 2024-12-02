import os
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_new_message(context, model_version, new_message):
    """
    Generates a response from the OpenAI API based on the provided context and new message.

    Parameters:
        context (list): A list of dictionaries representing the conversation history.
        model_version (str): The model version to use (e.g., 'gpt-3.5-turbo', 'gpt-4').
        new_message (str): The latest message input from the user.

    Returns:
        str: The generated response from the OpenAI API.
    """

    client = OpenAI(
        api_key=os.environ.get("OPEN_AI_TOKEN"),
    )

    if not client.api_key:
        raise ValueError("OPEN_AI_TOKEN environment variable not found.")

    context.append({"role": "user", "content": new_message})

    response = client.chat.completions.create(
        model=model_version,
        messages=context
    )
    choice = response.choices[0].message
    print(choice)

    # Extract the assistant's reply
    #assistant_reply = response['choices'][0]['message']['content'].strip()

    # Append the assistant's reply to the context
    #context.append({"role": "assistant", "content": assistant_reply})
#
    #return assistant_reply


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
