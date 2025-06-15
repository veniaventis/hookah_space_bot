from aiogram.fsm.state import StatesGroup, State


class OrderStates(StatesGroup):
    open_order = State()
    choose_menu = State()
    confirm_price = State()
    select_payment = State()
    pay_order = State()
    change_price = State()
    close_order = State()
    enter_custom_price = State()
    enter_comment = State()
