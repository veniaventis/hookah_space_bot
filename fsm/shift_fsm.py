from aiogram.fsm.state import State, StatesGroup


class ShiftStates(StatesGroup):
    # Открытие смены
    choose_point = State()
    enter_cash = State()
    confirm_cash = State()
    upload_tobacco_photo = State()
    confirm_tobacco_photo = State()
    working = State()

    # Закрытие смены
    enter_cash_report = State()
    enter_terminal_report = State()
    upload_remaining_tobacco = State()
    confirm_remaining_tobacco_photo = State()
    add_remaining_coals = State()
    extra_information = State()
    confirm_close_shift = State()

class OrderStates(StatesGroup):
    choose_menu = State()
    open_order = State()
    pay_order = State()
    close_order = State()
   # класс заказа

