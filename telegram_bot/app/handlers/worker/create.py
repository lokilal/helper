from aiogram import types


async def create_worker(call: types.CallbackQuery):
    await call.message.answer('Работникам привет!')
