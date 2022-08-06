from aiogram import types


def get_start_keyboard():
    buttons = [
        types.InlineKeyboardButton(text='Заказчик', callback_data='customer'),
        types.InlineKeyboardButton(text='Исполнитель', callback_data='worker')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
