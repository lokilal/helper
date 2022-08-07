from aiogram import types


def get_gender_keyboard():
    buttons = [
        types.InlineKeyboardButton(text='Мужчина', callback_data='M'),
        types.InlineKeyboardButton(text='Женщина', callback_data='F')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_profession_keyboard(professions):
    buttons = []
    for profession in professions:
        buttons.append(
            types.InlineKeyboardButton(
                text=profession,
                callback_data=profession)
        )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
