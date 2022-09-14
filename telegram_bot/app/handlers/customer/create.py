import os
import requests

from aiogram import types
from dotenv import load_dotenv

from app.keyboards.customer.menu import get_customer_menu_keyboard

load_dotenv()

HOST = os.getenv('HOST')


async def create_customer(call: types.CallbackQuery):
    response = requests.get(
        f'{HOST}/api/v1/customers/?telegram_id={call.message.chat.id}'
    )
    if response.status_code != 200:
        await call.message.answer('В данный момент проходят технические работы,'
                                  'просим прощения за доставленные неудобства.')
        return
    elif not response.json():
        context = {
            'name': call.message.chat.username,
            'telegram_id': call.message.chat.id
        }
        requests.post(
            f'{HOST}/api/v1/customers/',
            data=context
        )
    await call.message.edit_text('Отлично, теперь выбери, что тебе нужно'
                                 , reply_markup=get_customer_menu_keyboard())
