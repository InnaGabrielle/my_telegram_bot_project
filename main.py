import config
import logging
from aiogram import Bot, Dispatcher, types
import asyncio
from handlers import random_fact, celebrity, chat_gpt, quiz, recommendations, vocabulary_trainer
import openai
import os
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.keyboards import menu_kb
from aiogram.fsm.context import FSMContext

TOKEN_API = config.TOKEN_TG
OPENAI_API_KEY = config.OPENAI_API_KEY

async def main():


    # Logging setup
    logging.basicConfig(level=logging.INFO)

    # Bot and dispatcher initialisation
    bot = Bot(token=TOKEN_API)
    dp = Dispatcher()

    openai.api_key = OPENAI_API_KEY

    # /start command handler
    @dp.message(lambda msg: msg.text == "Back to Menu")
    @dp.message(Command("start"))
    @dp.message(Command("finish"))
    async def start(message: Message, state: FSMContext):
        await state.clear()  # Reset user state
        await message.answer(f"Hello, dear {message.chat.username}! Choose an option:", reply_markup=menu_kb)

    # Register routers
    dp.include_router(celebrity.router)
    dp.include_router(random_fact.router)
    dp.include_router(chat_gpt.router)
    dp.include_router(quiz.router)
    dp.include_router(recommendations.router)
    dp.include_router(vocabulary_trainer.router)


    # Start bot polling
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Bot stopped due to error: {e}")


if __name__=='__main__':
    asyncio.run(main())