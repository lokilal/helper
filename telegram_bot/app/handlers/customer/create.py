from aiogram import types
import requests


async def create_customer(call: types.CallbackQuery):
    context = {
        'name': call.message.chat.username,
        'telegram_id': call.message.chat.id
    }
    requests.post('http://127.0.0.1:8000/api/v1/customers/',
                  data=context)
    await call.message.answer(f'Добро пожаловать {context["name"]} в наше общество!')
