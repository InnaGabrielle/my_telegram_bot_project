from aiogram import Router, types
from aiogram.filters.command import Command
from utils.chat_gpt_service import ChatGPTService
import openai
from utils import end_chat


router = Router()
gpt_service = ChatGPTService()
gpt_service.set_system_message("You are a highly experienced Python developer with over 10 years of expertise in "
                               "software development, debugging, and best practices. You have a deep understanding "
                               "of Python frameworks, libraries, and optimization techniques. "
                               "Your goal is to assist the user by providing clear, efficient, "
                               "and well-structured explanations. When answering, ensure clarity, "
                               "provide code examples when needed, and suggest best practices. "
                               "If the user has a problem, guide them step by step toward a solution.")


# /gpt command starts the chat
@router.message(Command('gpt'))
async def command_gpt(message: types.Message):
    await message.answer(f'Hello, dear {message.chat.username}, please enter your request. I am a python developer with 10 years experience. I will try to help you')

# Handle messages for ChatGPT
@router.message()
async def handle_message(message: types.Message):
    # If user types "End Chat", terminate session
    if message.text.lower() == "end chat":
        await end_chat(message.bot, message.from_user.id)
        return
    gpt_service.add_user_message(message.text)
    response = gpt_service.get_response()

    # Send response with an "End Chat" button
    end_chat_button = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="End Chat")]],
        resize_keyboard=True
    )
    await message.answer(response, reply_markup=end_chat_button)


# Function to get ChatGPT response based on prompt
async def get_chatgpt_response(prompt):
    response = openai.completions.create(model= "gpt-4", prompt=prompt, max_tokens=500)
    return response.choices[0].text.strip()


