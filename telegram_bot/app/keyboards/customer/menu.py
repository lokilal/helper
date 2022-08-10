from aiogram import types


def get_customer_menu_keyboard():
    buttons = [
        types.InlineKeyboardButton(text='Подобрать специалиста', callback_data='specialists'),
        types.InlineKeyboardButton(text='Изменить анкету', callback_data='questionnaires')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_all_professions_keyboard(professions):
    buttons = []
    for profession in professions:
        buttons.append(
            types.InlineKeyboardButton(text=profession, callback_data=profession)
        )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_start_questionnaire_keyboard():
    buttons = [
        types.InlineKeyboardButton(
            text='Начать тестирование',
            callback_data='start_questionnaire'),
        types.InlineKeyboardButton(
            text='Вернуться в начало',
            callback_data='customer'
        )
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
