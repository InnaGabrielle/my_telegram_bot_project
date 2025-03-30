from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
import openai

router = Router()
# Dictionary to store user words
user_words = {}

async def get_new_word():
    content = "Provide a new word in English, its translation into another language (e.g., Spanish), and an example sentence."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": content}
        ]
    )
    return response["choices"][0]["message"]["content"]