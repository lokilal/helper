from .customer.create import create_customer
from .worker.create import create_worker
from aiogram.dispatcher.filters import Text


def get_all_handlers(dp):
    dp.register_callback_query_handler(create_customer, Text(contains='customer'))
    dp.register_callback_query_handler(create_worker, Text(contains='worker'))
