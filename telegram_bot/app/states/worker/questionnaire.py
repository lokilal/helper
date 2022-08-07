from aiogram.dispatcher.filters.state import State, StatesGroup


class QuestionnaireWorker(StatesGroup):
    telegram_id = State()
    name = State()
    gender = State()
    profession = State()
    experience = State()
    about = State()
