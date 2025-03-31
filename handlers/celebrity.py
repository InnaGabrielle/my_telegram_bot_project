from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
import openai
from states import UserState
from keyboards.keyboards import menu_kb, celebrity_kb


router = Router()

celebrities = ['Freddy Krueger', 'Pinhead', 'Chucky', 'Jigsaw']
# Dictionary mapping celebrities to their ChatGPT prompts
celebrity_prompts = {
    "Freddy Krueger": "You are Freddy Krueger, a terrifying dream demon with a dark sense of humor.",
    "Pinhead": "You are Pinhead, the leader of the Cenobites, speaking in a deep and philosophical tone.",
    "Chucky": "You are Chucky, the possessed killer doll, speaking with sarcasm and aggression.",
    "Jigsaw": "You are Jigsaw, a mastermind of deadly games, speaking cryptically and philosophically."
}

# Dictionary to track conversation history per user
user_histories = {}


# Handle "Chat with Celebrity" button and /talk command
@router.message(lambda msg: msg.text == "Chat with Celebrity")
@router.message(Command('talk'))
async def select_celebrity(message: types.Message, state: FSMContext):
    image1 = 'https://en.wikipedia.org/wiki/File:Freddy_Krueger_(Robert_Englund).jpg'
    image2 = 'https://static.wikia.nocookie.net/hellraiser/images/a/a5/Pinhead_Hell_Priest.jpg/revision/latest?cb=20190605194826'
    image3 = 'https://static.wikia.nocookie.net/antagonisten/images/5/52/Chucky.jpg/revision/latest?cb=20161203190717&path-prefix=de'
    image4 = 'https://static.wikia.nocookie.net/villains/images/3/3f/Jigsaw2.jpg/revision/latest?cb=20180522024024'
    await message.answer_photo(image1)
    await message.answer_photo(image2)
    await message.answer_photo(image3)
    await message.answer_photo(image4)
    await message.answer(f'Please choose a celebrity to chat with:', reply_markup=celebrity_kb)
    await state.set_state(UserState.CELEBRITY_CHAT)

# Handle celebrity selection
@router.message(lambda msg: msg.text in celebrity_prompts.keys())
async def chosen_celebrity(message: types.Message, state: FSMContext):
    chosen_celeb = message.text
    await state.update_data(celebrity=chosen_celeb) # Store selection in FSM
    await message.answer(f"You have chosen {chosen_celeb}. Now start chatting!")


# Handle user messages in "Chat with Celebrity" mode
@router.message(UserState.CELEBRITY_CHAT)
async def handle_celebrity_chat(message: types.Message, state: FSMContext):
    user_input = message.text

    # Check if user wants to finish chat
    if user_input == "/finish":
        await finish_chat(message, state)
        return

    data = await state.get_data()
    chosen_celeb = data.get("celebrity")

    if chosen_celeb not in celebrity_prompts:
        await message.answer("Please choose a celebrity first!", reply_markup=celebrity_kb)
        return

    system_prompt = celebrity_prompts[chosen_celeb]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": user_input}]
    )

    chat_reply = response["choices"][0]["message"]["content"]
    await message.answer(chat_reply)

# Handle /finish command to exit chat mode
@router.message(Command("finish"))
async def finish_chat(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Chat session ended. Choose an option:", reply_markup=menu_kb)

## Handle "Back to Menu" button
#@router.message(lambda msg: msg.text == "Back to Menu")
#async def back_to_menu(message: types.Message, state: FSMContext):
#    await state.clear()
#    await message.answer("Back to main menu:", reply_markup=menu_kb)
#
