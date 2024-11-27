from aiogram.fsm.state import State, StatesGroup


class ShiftStates(StatesGroup):
    choose_point = State()
    enter_cash = State()
    enter_tobacco = State()
    working = State()

class OrderStates(StatesGroup):
    choose_menu = State()
    choose_flavor = State()
    apply_discount = State()
    open_order = State()
    pay_order = State()
    close_order = State()