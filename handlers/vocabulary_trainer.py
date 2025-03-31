from aiogram import Router, types, F

import openai

router = Router()
# Dictionary to store user words
user_words = {}

async def get_new_word():
    content = "Provide a new word in English, its translation into another language, and an example sentence."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": content}
        ]
    )
    return response["choices"][0]["message"]["content"]

#TODO: implement vocabulary trainer