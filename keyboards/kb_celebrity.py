from aiogram import types


button_1 = types.KeyboardButton(text = '/talk')
button_2 = types.KeyboardButton(text ='/freddy_krueger')
button_3 = types.KeyboardButton(text ='/pinhead')
button_4 = types.KeyboardButton(text ='/chucky')
button_5 = types.KeyboardButton(text ='/jigsaw')

keyboard_1 = [[button_2, button_3], [button_4, button_5]]

kb_celeb = types.ReplyKeyboardMarkup(keyboard=keyboard_1, resize_keyboard=True)


