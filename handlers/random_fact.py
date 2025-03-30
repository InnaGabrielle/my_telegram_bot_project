from aiogram import Router, types, F
from aiogram.filters.command import Command
import random
import openai
from keyboards.keyboards import random_fact_kb, menu_kb
from aiogram.fsm.context import FSMContext

router = Router()
prompt_random = [
        "Tell me a fun and lesser-known fact about Python programming.",
        "Give me an interesting Python fact that most people don’t know.",
        "Share a surprising fact about the Python programming language.",
        "What’s a cool historical fact about Python?",
        "Provide a fascinating detail about Python’s design or syntax.",
    ]



# Function to generate a random Python fact using ChatGPT
async def get_random_fact():
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": random.choice(prompt_random)}
        ]
    )
    return response["choices"][0]["message"]["content"]

# /random
@router.message(Command('random'))
@router.message(lambda msg: msg.text == "Random Fact")
@router.message(lambda msg: msg.text == "Another Random Fact")
async def random_fact(message: types.Message, state: FSMContext):
    image = "https://lacvets.com/wp-content/uploads/2023/01/what-is-a-cats-lifespan-lakeland-fl-300x200.jpg"
    await message.answer_photo(image)
    await state.set_state("FACT_MODE")  # Set FSM state
    response = await get_random_fact()
    await message.answer(f"💡 Python Fact:\n{response}", reply_markup=random_fact_kb)


## Handle /finish command and "Back to Menu" button
#@router.message(Command("finish"))
#@router.message(lambda msg: msg.text == "Back to Menu")
#async def finish_fact_session(message: types.Message, state: FSMContext):
#    await state.clear()  # Reset user state
#    await message.answer("Fact session ended. Back to main menu:", reply_markup=menu_kb)
#
