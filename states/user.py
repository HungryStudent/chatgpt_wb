from aiogram.dispatcher.filters.state import StatesGroup, State


class DataStates(StatesGroup):
    enter_symbols_count = State()
    enter_name = State()
    enter_keys = State()
