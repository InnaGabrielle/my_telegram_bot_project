import config
import logging
from aiogram import Bot, Dispatcher
import asyncio
from handlers import random_fact, celebrity, chat_gpt
import openai



async def main():
    TOKEN_API = config.TOKEN_TG
    OPENAI_API_KEY = config.OPENAI_API_KEY

    # Logging setup
    logging.basicConfig(level=logging.INFO)

    # Bot and dispatcher initialisation
    bot = Bot(token=TOKEN_API)
    dp = Dispatcher()

    openai.api_key = OPENAI_API_KEY

    dp.include_router(celebrity.router)
    dp.include_router(random_fact.router)
    dp.include_router(chat_gpt.router)


    # Start bot polling
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Bot stopped due to error: {e}")


if __name__=='__main__':
    asyncio.run(main())