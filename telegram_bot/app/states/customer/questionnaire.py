from aiogram.dispatcher.filters.state import State, StatesGroup


class QuestionnaireCustomer(StatesGroup):
    telegram_id = State()
    questions = State()
    lasts_question = State()
    answers = State()
