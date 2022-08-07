from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import Dispatcher

from .customer.create import create_customer
from .customer.professions import select_specialist
from .worker.create import register_create_handlers


def get_all_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(create_customer, Text(contains='customer'))
    register_create_handlers(dp)
    dp.register_callback_query_handler(select_specialist, Text(contains='specialists'))
