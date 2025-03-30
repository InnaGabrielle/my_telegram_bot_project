from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Main menu keyboard
menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Random Fact"), KeyboardButton(text="Chat with Celebrity"), KeyboardButton(text="Ask ChatGPT"), KeyboardButton(text="Quiz")],
    ],
    resize_keyboard=True
)

# Celebrity selection keyboard
celebrity_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Freddy Krueger"), KeyboardButton(text="Pinhead")],
        [KeyboardButton(text="Chucky"), KeyboardButton(text="Jigsaw")],
        [KeyboardButton(text="Back to Menu")],
    ],
    resize_keyboard=True
)

# Random fact keyboard
random_fact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Another Random Fact")],
        [KeyboardButton(text="Back to Menu")]
    ],
    resize_keyboard=True
)
# ChatGPT keyboard
chat_gpt_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Back to Menu")]
    ],
    resize_keyboard=True
)

# Keyboard for quiz topics
topic_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Music")],
        [KeyboardButton(text="Geography")],
        [KeyboardButton(text="Python Programming")],
        [KeyboardButton(text="History")],
        [KeyboardButton(text="Back to Menu")]
    ],
    resize_keyboard=True
)

# Keyboard for quiz answers and stopping the quiz
quiz_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Next Question")],
        [KeyboardButton(text="Stop Quiz")],
        [KeyboardButton(text="Back to Menu")]
    ],
    resize_keyboard=True
)