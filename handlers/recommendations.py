import openai
import re
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import category_kb
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from states import RecommendationState

router = Router()




# Handle /recommend command and Button to start recommendation session
@router.message(Command("recommend"))
@router.message(lambda msg: msg.text == "Recommendations")
async def start_recommendation(message: Message, state: FSMContext):
    await state.set_state(RecommendationState.choosing_category)
    await message.answer("What kind of recommendations do you want?", reply_markup=category_kb)


# Handle category selection. It registers a function to handle callback queries (button pressed from inline keyboards,
# see keyboard definition in keyboards.py).
# In Aiogram, when a user presses an inline button, the bot receives a callback query instead of a regular message.
# This decorator ensures that the bot listens for specific callback queries.
@router.callback_query(lambda c: c.data.startswith("category_")) # c is the callback query object; c.data is the data payload of the clicked button. This data was defined when the button was created ("category_movies", "category_books").
async def choose_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[1]  # Extract 'movies', 'books', or 'music'
    await state.update_data(category=category, disliked_items=[])
    await state.set_state(RecommendationState.choosing_genre) # setting the state "choosing_genre"
    await callback.message.edit_text(
        f"You chose \"{category.capitalize()}\". Now, enter a genre (e.g., 'sci-fi', 'romance', 'rock').")


# Message handler that listens for user messages when the bot is in the "choosing_genre"-state
@router.message(RecommendationState.choosing_genre)
async def get_genre(message: Message, state: FSMContext):
    genre = message.text.strip().lower()
    await state.update_data(genre=genre)
    # after extraction the genre from the user's message update the state:
    await state.set_state(RecommendationState.receiving_recommendation)
    await fetch_recommendation(message, state)


# Function to fetch recommendation from ChatGPT
async def fetch_recommendation(message: Message, state: FSMContext):
    data = await state.get_data()
    category = data.get("category")
    genre = data.get("genre")
    disliked_items = data.get("disliked_items", [])

    # Construct AI prompt
    prompt = f"Suggest a {category} in the {genre} genre. Avoid these: {', '.join(disliked_items)}. Provide only the name."

    # Get response from ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a recommendation assistant. Suggest only one title per request."},
            {"role": "user", "content": prompt}
        ]
    )

    recommendation = response["choices"][0]["message"]["content"].strip()

    # Update state with new recommendation
    await state.update_data(last_recommendation=recommendation)

    # Send recommendation with "Dislike" button
    dislike_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👎 Dislike", callback_data="dislike")],
            [InlineKeyboardButton(text="Back to Menu", callback_data="back_to_menu")]
        ]
    )

    await message.answer(f"Recommended {category.capitalize()}: \"{recommendation}\"", reply_markup=dislike_kb)


# Handle dislike button click
@router.callback_query(lambda c: c.data == "dislike")
async def dislike_recommendation(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    last_recommendation = data.get("last_recommendation")
    disliked_items = data.get("disliked_items", [])

    # Add disliked item to the list
    if last_recommendation not in disliked_items:
        disliked_items.append(last_recommendation)
        await state.update_data(disliked_items=disliked_items)

    # Fetch a new recommendation avoiding disliked ones
    await fetch_recommendation(callback.message, state)


# Handle returning to menu
@router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Returning to main menu", reply_markup=None)
