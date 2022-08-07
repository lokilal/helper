import requests

from aiogram import types

from app.keyboards.customer.menu import get_all_professions_keyboard


async def select_specialist(call: types.CallbackQuery):
    response = requests.get(
        'http://127.0.0.1:8000/api/v1/professions/'
    ).json()
    professions = []
    for profession in response:
        professions.append(profession['title'])
    await call.message.edit_text(
        'Выберите нужного специалиста', reply_markup=get_all_professions_keyboard(professions)
    )
