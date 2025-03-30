from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from states import UserState
from keyboards.keyboards import chat_gpt_kb
import openai
from utils import end_chat


router = Router()
#gpt_service = ChatGPTService()
#gpt_service.set_system_message("You are a highly experienced Python developer with over 10 years of expertise in "
#                               "software development, debugging, and best practices. You have a deep understanding "
#                               "of Python frameworks, libraries, and optimization techniques. "
#                               "Your goal is to assist the user by providing clear, efficient, "
#                               "and well-structured explanations. When answering, ensure clarity, "
#                               "provide code examples when needed, and suggest best practices. "
#                               "If the user has a problem, guide them step by step toward a solution.")
#

# /gpt command starts the chat
@router.message(Command('gpt'))
@router.message(lambda msg: msg.text == "Ask ChatGPT")
async def start_chat_gpt(message: types.Message, state: FSMContext):
    await state.set_state(UserState.CHAT_GPT)
    await state.update_data(history=[])  # Store chat history
    await message.answer(f'ChatGPT session started! Ask me anything:', reply_markup=chat_gpt_kb)

# Handle user messages in ChatGPT session
@router.message(UserState.CHAT_GPT)
async def chat_with_gpt(message: types.Message, state: FSMContext):
    data = await state.get_data()
    history = data.get("history", [])

    # Append user message to conversation history
    history.append({"role": "user", "content": message.text})

    # Generate response from ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history
    )

    bot_reply = response["choices"][0]["message"]["content"]
    history.append({"role": "assistant", "content": bot_reply})

    # Save updated conversation history
    await state.update_data(history=history)

    # Send ChatGPT response
    await message.answer(bot_reply, reply_markup=chat_gpt_kb)

## Handle messages for ChatGPT
#@router.message()
#async def handle_message(message: types.Message):
#    # If user types "End Chat", terminate session
#    if message.text.lower() == "end chat":
#        await end_chat(message.bot, message.from_user.id)
#        return
#    gpt_service.add_user_message(message.text)
#    response = gpt_service.get_response()
#
#    # Send response with an "End Chat" button
#    end_chat_button = types.ReplyKeyboardMarkup(
#        keyboard=[[types.KeyboardButton(text="End Chat")]],
#        resize_keyboard=True
#    )
#    await message.answer(response, reply_markup=end_chat_button)
#
#
## Function to get ChatGPT response based on prompt
#async def get_chatgpt_response(prompt):
#    response = openai.completions.create(model= "gpt-4", prompt=prompt, max_tokens=500)
#    return response.choices[0].text.strip()
#

