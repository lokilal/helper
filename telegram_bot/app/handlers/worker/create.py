import requests
import os

from aiogram.dispatcher.filters import Text
from aiogram import types, dispatcher
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv

from app.keyboards.worker.create import get_gender_keyboard, get_profession_keyboard
from app.states.worker.questionnaire import QuestionnaireWorker

load_dotenv()

HOST = os.getenv('HOST')


professions = requests.get(
    f'{HOST}/api/v1/professions/'
).json()

GENDERS = ['F', 'M']
PROFESSIONS = [profession['title'] for profession in professions]


def send_post_request(user_data):
    context = {
        'telegram_id': user_data['telegram_id'],
        'name': user_data['name'],
        'gender': user_data['gender'],
        'profession': user_data['profession'],
        'experience': user_data['experience'],
        'about': user_data['about']
    }
    requests.post(
        f'{HOST}/api/v1/workers/',
        data=context
    )


async def create_worker(call: types.CallbackQuery):
    await call.message.answer('Приветствую, работяга!')
    response = requests.get(
        f'{HOST}/api/v1/workers/?telegram_id={call.message.chat.id}'
    )
    if response.status_code != 200:
        await call.message.edit_text('В данный момент проходят технические работы,'
                                     'просим прощения за доставленные неудобства.')
    elif not response.json():
        await call.message.answer('Для начала введите имя, которое будет отображаться '
                                  'в вашем профиле')
        await QuestionnaireWorker.name.set()
    else:
        await call.message.answer('Вы зарегистрированы')


async def get_name(message: types.Message, state: FSMContext):
    if len(message.text) < 2:
        await message.answer('Имя не может состоять из одного знака')
        return
    await state.update_data(name=message.text,
                            telegram_id=message.from_user.id)
    await message.answer('Теперь выберите ваш пол', reply_markup=get_gender_keyboard())
    await QuestionnaireWorker.next()


async def get_gender(call: types.CallbackQuery, state: FSMContext):
    if call.data not in GENDERS:
        await call.answer('Пожалуйста, выберите пол ,используя '
                          'клавиатуру ниже.')
        return
    await state.update_data(gender=call.data)
    await call.message.edit_text('Теперь выбери свою профессию',
                                 reply_markup=get_profession_keyboard(PROFESSIONS)
                                 )
    await QuestionnaireWorker.profession.set()


async def get_profession(call: types.CallbackQuery, state: FSMContext):
    if call.data not in PROFESSIONS:
        await call.answer('Пожалуйста, выберите профессию ,используя '
                          'клавиатуру ниже.')
        return
    await state.update_data(profession=call.data)
    await call.message.answer('Введите ваш опыт в годах')
    await QuestionnaireWorker.experience.set()


async def get_experience(message: types.Message, state: FSMContext):
    try:
        if float(message.text) < 2:
            await message.answer('Нам нужны специалисты с опытом больше'
                                 ' чем два года')
        else:
            await state.update_data(experience=message.text)
            await message.answer('Отлично, теперь напишите пару предложений о себе')
            await QuestionnaireWorker.about.set()
    except ValueError:
        await message.answer('Вы вводите не цифры')


async def get_about(message: types.Message, state: FSMContext):
    if len(message.text) < 120:
        await message.answer('Вы написали очень мало о себе, этого недостаточно')
        return
    await state.update_data(about=message.text)
    await message.answer('Отлично, вы ответили на все вопросы. В ближайшее время '
                         'модерация проверит ваш профиль и ответит вам')
    user_data = await state.get_data()
    send_post_request(user_data)
    await state.finish()


def register_create_handlers(dp: dispatcher.Dispatcher):
    dp.register_callback_query_handler(
        create_worker,
        Text(contains='worker'))
    dp.register_message_handler(get_name, state=QuestionnaireWorker.name)
    dp.register_callback_query_handler(
        get_gender,
        state=QuestionnaireWorker.gender
    )
    dp.register_callback_query_handler(
        get_profession, state=QuestionnaireWorker.profession
    )
    dp.register_message_handler(
        get_experience,
        state=QuestionnaireWorker.experience)
    dp.register_message_handler(
        get_about, state=QuestionnaireWorker.about
    )
