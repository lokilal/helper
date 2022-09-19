from aiogram import types


def get_question_keyboard(choices: dict):
    buttons = []
    for choice in choices:
        buttons.append(
            types.InlineKeyboardButton(
                text=choice['title'], callback_data=choice['title']
            )
        )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
