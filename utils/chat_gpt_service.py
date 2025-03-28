import openai

async def get_chatgpt_response(history):
    """Sends the conversation history to ChatGPT and returns its response."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=history
    )
    return response["choices"][0]["message"]["content"]


async def get_chatgpt_response(prompt):
    """Sends a single prompt to ChatGPT and returns the response."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Provide a random fact in an engaging way."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]



import openai
import os

from pyexpat.errors import messages

import config

token = os.getenv('OPENAI_API_KEY')
openai.api_key = token

class ChatGPTService:
    def __init__(self):
        self.message_history = []

    def set_system_message(self, content):
        self.message_history.append({"role": "system", "content": content})

    def add_assistant_message(self, content):
        self.message_history.append({"role": "assistant", "content": content})

    def add_user_message(self, user_content):
        self.message_history.append({"role": "user", "content": user_content})

    def get_response(self, model="gpt-4", temperature=0.5):
        response = openai.ChatCompletion.create(model=model,
                                                messages=self.message_history,
                                                temperature=temperature,
                                                max_tokens=1000)
        assistant_reply = response['choices'][0]['message']['content']
        self.add_assistant_message(assistant_reply)
        return assistant_reply