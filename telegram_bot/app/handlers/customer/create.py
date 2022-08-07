import requests

from aiogram import types

from app.keyboards.customer.menu import get_customer_menu_keyboard


async def create_customer(call: types.CallbackQuery):
    context = {
        'name': call.message.chat.username,
        'telegram_id': call.message.chat.id
    }
    requests.post('http://127.0.0.1:8000/api/v1/customers/',
                  data=context)
    await call.message.edit_text(
        f'Добро пожаловать {context["name"]} в наше общество! '
        f'Выбери, что тебе нужно',
        reply_markup=get_customer_menu_keyboard()
    )
