from aiogram import types


def get_create_keyboard():
    buttons = [
        types.InlineKeyboardButton(text='Мужчина', callback_data='M'),
        types.InlineKeyboardButton(text='Женщина', callback_data='F')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
