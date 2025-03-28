from aiogram import Router, types, F
from aiogram.filters.command import Command
#from handlers.chat_gpt import get_chatgpt_response
from utils.chat_gpt_service import get_chatgpt_response

from keyboards.kb_random import kb1
from keyboards.kb_celebrity import kb_celeb

router = Router()
prompt_random = "Give me a true random fact about programming in python"

# /start
@router.message(Command('start'))
@router.message(Command('finish'))
async def command_start(message: types.Message):
    await message.answer(f'Hello, dear {message.chat.username}, I am javarush bot', reply_markup=kb1)

# /random
@router.message(Command('random'))
@router.message(Command('another_random_fact'))
async def command_start(message: types.Message):
    image = "https://lacvets.com/wp-content/uploads/2023/01/what-is-a-cats-lifespan-lakeland-fl-300x200.jpg"
    await message.answer_photo(image)
    response = await get_chatgpt_response(prompt=prompt_random)
    await message.answer(response, reply_markup=kb1)



@router.message(F.text)
async def echo(message: types.Message):
    print(message.text)
    if 'stop' in message.text:
        await message.answer('ok, as you wish')
    else:
        await message.answer(message.text)


