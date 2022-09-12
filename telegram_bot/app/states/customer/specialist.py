from aiogram.dispatcher.filters.state import State, StatesGroup


class SpecialistChoice(StatesGroup):
    """
        Класс хранит в себе следующие данные пользователя:
        какого специалиста он ищет, предыдущая и следующая страница с работниками
    """
    profession = State()
    next_page = State()
    previous_page = State()
