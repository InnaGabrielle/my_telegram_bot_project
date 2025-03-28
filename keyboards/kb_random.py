from aiogram import types

button_1 = types.KeyboardButton(text = '/start')
button_2 = types.KeyboardButton(text ='/another_random_fact')
button_3 = types.KeyboardButton(text ='/finish')
button_4 = types.KeyboardButton(text ='/stop')

keyboard_1 = [[button_2, button_3]]
keyboard_2 = [[button_1, button_4], [button_2, button_3]]

kb1 = types.ReplyKeyboardMarkup(keyboard=keyboard_1, resize_keyboard=True)
kb2 = types.ReplyKeyboardMarkup(keyboard=keyboard_2, resize_keyboard=True)