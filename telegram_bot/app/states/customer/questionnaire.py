from aiogram.dispatcher.filters.state import State, StatesGroup


class QuestionnaireCustomer(StatesGroup):
    """
        Класс отвечает за ответы на тестирование
    """
    telegram_id = State()
    questions = State()
    lasts_question = State()
    answers = State()
