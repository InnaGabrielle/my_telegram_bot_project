from aiogram import Bot, types

# Dictionary to track conversation history per user
user_histories = {}

async def end_chat(bot: Bot, user_id: int):
    """Ends the chat session for a user, clearing their history."""
    user_histories.pop(user_id, None)  # Remove user chat history

    # Send message to the user
    await bot.send_message(user_id, "Chat ended. Use \n -/talk \n -/gpt \n -/random \n to start again.", reply_markup=types.ReplyKeyboardRemove())