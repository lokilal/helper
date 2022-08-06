import requests

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, dispatcher
from aiogram.dispatcher import FSMContext

from app.keyboards.worker.create import get_create_keyboard


GENDERS = ['F', 'M']


class QuestionnaireWorker(StatesGroup):
    name = State()
    gender = State()
    profession = State()
    experience = State()
    about = State()


async def create_worker(call: types.CallbackQuery):
    await call.message.answer('Приветствую, работяга, необходимо пройти'
                              'небольшой опрос')
    await call.message.answer('Для начала введите имя, которое будет отображаться '
                              'в вашем профиле')
    await QuestionnaireWorker.name.set()


async def get_name(message: types.Message, state: FSMContext):
    if len(message.text) < 2:
        await message.answer('Имя не может состоять из одного знака')
        return
    await state.update_data(name=message.text)
    await QuestionnaireWorker.next()
    await message.answer('Теперь выберите ваш пол', reply_markup=get_create_keyboard())


async def get_gender(call: types.CallbackQuery, state: FSMContext):
    if call.data not in GENDERS:
        await call.answer('Пожалуйста, выберите пол ,используя '
                          'клавиатуру ниже.')
        return
    await state.update_data(gender=call.data)


def register_create_handlers(dp: dispatcher.Dispatcher):
    dp.register_callback_query_handler(create_worker, Text(contains='worker'))
    dp.register_message_handler(get_name, state=QuestionnaireWorker.name)
    dp.register_callback_query_handler(
        get_gender,
        state=QuestionnaireWorker.gender
    )
