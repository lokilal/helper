import requests

from aiogram import types, dispatcher
from aiogram.dispatcher.filters import Text

from app.keyboards.customer.menu import get_all_professions_keyboard

response = requests.get(
    'http://127.0.0.1:8000/api/v1/professions/'
).json()
PROFESSIONS = [profession['title'] for profession in response]


async def select_specialist(call: types.CallbackQuery):
    await call.message.edit_text(
        'Выберите нужного специалиста',
        reply_markup=get_all_professions_keyboard(PROFESSIONS)
    )


async def chose_specialist(call: types.CallbackQuery):
    requests.get(
        f'http://127.0.0.1:8000/api/v1/customers/{call.message.chat.id}/'
    )



def chose_specialist_handlers(dp: dispatcher.Dispatcher):
    for profession in PROFESSIONS:
        dp.register_callback_query_handler(
            chose_specialist, Text(contains=profession)
        )
