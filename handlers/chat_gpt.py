from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
import openai
from states import UserState
from keyboards.keyboards import chat_gpt_kb


router = Router()

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

