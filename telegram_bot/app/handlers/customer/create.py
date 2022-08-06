from aiogram import types


async def create_customer(call: types.CallbackQuery):
    await call.message.answer('Привет обычным пользователям!')
