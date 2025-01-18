from aiogram.filters.state import StatesGroup, State


class RegisterState(StatesGroup):
    phone_number = State()
    jshshir = State()

class UserState(StatesGroup):
    main = State()
    settings = State()
    get_month = State()


class SettingsState(StatesGroup):
    phone_number = State()
    jshshir = State()

class AdminState(StatesGroup):
    upload_file = State()
    delete_file = State()
