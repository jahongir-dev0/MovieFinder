from aiogram import Dispatcher
from loader import dp
from .admin_filter import AdminFilter

if __name__ == "__main__":
    dp.filters_factory.bind(AdminFilter)