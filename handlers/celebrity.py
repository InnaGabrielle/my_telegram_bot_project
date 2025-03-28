from aiogram import Router, types, F
from aiogram.filters.command import Command
from keyboards.kb_celebrity import kb_celeb
from aiogram.fsm.context import FSMContext
from keyboards.prof_keyboards import make_row_keyboard
from aiogram.fsm.state import State, StatesGroup
from utils import chat_gpt_service
import openai

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

# States for FSM
class CelebrityChoice(StatesGroup):
    celebrity = State()
    chatting = State()



@router.message(Command('talk'))
async def command_talk(message: types.Message, state: FSMContext):

    image1 = 'https://en.wikipedia.org/wiki/File:Freddy_Krueger_(Robert_Englund).jpg'
    image2 = 'https://static.wikia.nocookie.net/hellraiser/images/a/a5/Pinhead_Hell_Priest.jpg/revision/latest?cb=20190605194826'
    image3 = 'https://static.wikia.nocookie.net/antagonisten/images/5/52/Chucky.jpg/revision/latest?cb=20161203190717&path-prefix=de'
    image4 = 'https://static.wikia.nocookie.net/villains/images/3/3f/Jigsaw2.jpg/revision/latest?cb=20180522024024'
    await message.answer_photo(image1)
    await message.answer_photo(image2)
    await message.answer_photo(image3)
    await message.answer_photo(image4)
    await message.answer(f'Hello, {message.chat.username}, choose your favourite celebrity', reply_markup=make_row_keyboard(celebrities))
    await state.set_state(CelebrityChoice.celebrity)


@router.message(CelebrityChoice.celebrity, F.text.in_(celebrities))
async def celeb_chosen(message: types.Message, state: FSMContext):
    await state.update_data(celebrity=message.text)
    user_data = await state.get_data()
    # Initialize message history with system role
    user_histories[message.from_user.id] = [{"role": "system", "content": celebrity_prompts[user_data["celebrity"]]}]

    await message.answer(
        f'You have chosen: {user_data["celebrity"]}. Now start chatting!',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(CelebrityChoice.chatting)
    #await state.clear()



@router.message(CelebrityChoice.celebrity)
async def celeb_incorrect(message: types.Message):
    await message.answer('Choose your favourite celebrity from the GIVEN list', reply_markup=make_row_keyboard(celebrities))

@router.message(F.text == "End Chat")
async def end_chat(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Clear stored data
    user_histories.pop(user_id, None)
    await state.clear()
    await message.answer("Chat ended. Use \n -/talk \n -/gpt \n -/random \n to start again.", reply_markup=types.ReplyKeyboardRemove())

@router.message(CelebrityChoice.chatting)
async def chat_with_celebrity(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Ensure message history exists
    if user_id not in user_histories:
        await message.answer("An error occurred. Please use /talk again.")
        return

    # Append user's message to chat history
    user_histories[user_id].append({"role": "user", "content": message.text})


    # Call OpenAI API with full conversation history
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=user_histories[user_id]
    )


    # Extract AI response and append it to history
    bot_reply = response.choices[0].message.content
    user_histories[user_id].append({"role": "assistant", "content": bot_reply})

    # Send response with "End Chat" button
    end_chat_button = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="End Chat")]],
        resize_keyboard=True
    )

    await message.answer(bot_reply, reply_markup=end_chat_button)
