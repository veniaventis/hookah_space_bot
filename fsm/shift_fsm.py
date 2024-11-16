from aiogram.fsm.state import State, StatesGroup


class ShiftStates(StatesGroup):
    choose_point = State()
    enter_cash = State()
    confirm_cash = State()
    upload_tobacco_photo = State()
    confirm_tobacco_photo = State()
    working = State()