import requests

from aiogram import types, dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State

from app.states.customer.questionnaire import QuestionnaireCustomer
from app.keyboards.customer.questionnaire import get_question_keyboard

response = requests.get(
    f'http://127.0.0.1:8000/api/v1/questions/'
).json()
QUESTIONS_CHOICES = [question['choices'] for question in response if question['question_type'] == 'checkbox']


async def checkbox_questionnaire_answer(call: types.CallbackQuery):
    if call.data not in ('start_questionnaire', 'customer_next_question'):
        QuestionnaireCustomer.answers.append(
            {'title': call.data}
        )
    else:
        if call.data == 'customer_next_question':
            if len(QuestionnaireCustomer.answers) == 0:
                await call.answer('Вы не выбрали ответ')
            else:
                context = {
                    'customer': call.message.chat.id,
                    'question': QuestionnaireCustomer.lasts_question,
                    'choice': [
                        *QuestionnaireCustomer.answers
                    ]
                }
                question_answer = requests.post(
                    f'http://127.0.0.1:8000/api/v1/answers/',
                    json=context
                )
                if question_answer.status_code != 201:
                    await call.answer('Технические неполадки')
                    return
                QuestionnaireCustomer.answers = []
        if isinstance(QuestionnaireCustomer.questions, State):
            await call.answer('Что-то пошло не так. Прошу вернуться в начало командой /start')
            return
        else:
            if len(QuestionnaireCustomer.questions) != 0:
                question = QuestionnaireCustomer.questions.pop(0)
                QuestionnaireCustomer.lasts_question = question['title']
                if question['question_type'] == 'checkbox':
                    await call.message.edit_text(
                        question['title'],
                        reply_markup=get_question_keyboard(question['choices'])
                    )
                else:
                    print('Текстовый вопрос')
            else:
                await call.answer('Программист')


def questionnaire_answers_handlers(dp: dispatcher.Dispatcher):
    dp.register_callback_query_handler(
        checkbox_questionnaire_answer,
        Text(
            contains='customer_next_question',
        ))
    dp.register_callback_query_handler(
        checkbox_questionnaire_answer,
        Text(
            contains='start_questionnaire',
        ))
    for question_choice in QUESTIONS_CHOICES:
        for choice in question_choice:
            dp.register_callback_query_handler(
                checkbox_questionnaire_answer,
                Text(contains=choice['title'])
            )
