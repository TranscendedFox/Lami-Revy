import os
import openai

from openai import OpenAI

# ENTER KEY
os.environ[
    "OPENAI_API_KEY"] = ""

client = OpenAI()


def get_response(messages_buffer):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_buffer
        )
        return response.choices[0].message.content
    except Exception as e:
        error_message = "There was a connection error. Please try again later."
        return error_message
