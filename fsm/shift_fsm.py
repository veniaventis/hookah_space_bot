from aiogram.fsm.state import State, StatesGroup


class ShiftStates(StatesGroup):
    choose_point = State()
    enter_cash = State()
    enter_tobacco = State()
    working = State()