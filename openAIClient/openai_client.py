import os
import openai

from openai import OpenAI

# ENTER KEY
os.environ[
    "OPENAI_API_KEY"] = ""

client = OpenAI()


def get_response(messages_buffer):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_buffer
    )
    return response.choices[0].message.content
