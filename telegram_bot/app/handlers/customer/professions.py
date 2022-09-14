import requests
import os

from aiogram import types, dispatcher
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv

from app.keyboards.customer.menu import get_all_professions_keyboard, get_start_questionnaire_keyboard
from app.states.customer.questionnaire import QuestionnaireCustomer
from app.states.customer.specialist import SpecialistChoice

load_dotenv()

HOST = os.getenv('HOST')

response = requests.get(
    f'{HOST}/api/v1/professions/'
).json()
PROFESSIONS = [profession['title'] for profession in response]


async def select_specialist(call: types.CallbackQuery):
    await call.message.edit_text(
        'Выберите нужного специалиста',
        reply_markup=get_all_professions_keyboard(PROFESSIONS)
    )


async def chose_specialist(call: types.CallbackQuery):
    user_questionnaires = requests.get(
        f'{HOST}/api/v1/customers/?telegram_id={call.message.chat.id}'
    )
    if user_questionnaires.status_code != 200:
        await call.message.answer('В данный момент проходят технические работы,'
                                  'просим прощения за доставленные неудобства.')
        return
    SpecialistChoice.profession = call.data
    if call.data not in user_questionnaires.json()[0]['questionnaires']:
        await call.message.edit_text(
            'Вы не ответили на анкету, жмите кнопку ниже',
            reply_markup=get_start_questionnaire_keyboard())
        questions = requests.get(
            f'{HOST}/api/v1/questions/?profession={call.data}'
        ).json()
        QuestionnaireCustomer.telegram_id = call.message.chat.id
        QuestionnaireCustomer.questions = questions
        QuestionnaireCustomer.answers = []
    else:
        await call.message.answer('Вы успешно прошли это анкетирование')


def chose_specialist_handlers(dp: dispatcher.Dispatcher):
    for profession in PROFESSIONS:
        dp.register_callback_query_handler(
            chose_specialist, Text(contains=profession)
        )
