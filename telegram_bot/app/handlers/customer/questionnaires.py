import requests
import os

from aiogram import types, dispatcher
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv

from app.states.customer.questionnaire import QuestionnaireCustomer
from app.keyboards.customer.questionnaire import get_question_keyboard

load_dotenv()

HOST = os.getenv('HOST')

response = requests.get(
    f'{HOST}/api/v1/questions/'
).json()
QUESTIONS = [question['choices'] for question in response]

CALL_DATA = []


async def checkbox_questionnaire_answer(call: types.CallbackQuery):
    if call.data in (*CALL_DATA, 'start_questionnaire') and len(QuestionnaireCustomer.questions) != 0:
        question = QuestionnaireCustomer.questions.pop(0)
        context = {
            'customer': call.message.chat.id,
            'question': question,
            'choice': [
                {'title': call.data}
            ]
        }
        question_answer = requests.post(
            f'{HOST}/api/v1/answers/',
            json=context
        )
        await call.message.edit_text(
            question['title'],
            reply_markup=get_question_keyboard(question['choices'])
        )
    else:
        await call.message.edit_text(
            'Большое спасибо за предоставленные ответы, с их помощью специалист '
            'сможет лучше разобраться в вашей проблеме. Перейдем к выбору специалистов'
        )


def questionnaire_answers_handlers(dp: dispatcher.Dispatcher):
    dp.register_callback_query_handler(
        checkbox_questionnaire_answer,
        Text(
            contains='start_questionnaire',
        ))
    for question_choice in QUESTIONS:
        for choice in question_choice:
            CALL_DATA.append(choice['title'])
            dp.register_callback_query_handler(
                checkbox_questionnaire_answer,
                Text(contains=choice['title'])
            )
