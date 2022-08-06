import asyncio

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from app.keyboards.common.start_keyboard import get_start_keyboard

from app.handlers import register_handlers


async def start_command(message: types.Message):
    await message.answer('Приветствую тебя, выбери кем ты являешься',
                         reply_markup=get_start_keyboard())


async def main():
    bot = Bot('1555030253:AAFfz7XlY14RrRDyrw0qqscI573MHekjPRU')
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.register_message_handler(start_command, commands='start')
    register_handlers.get_all_handlers(dp)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
