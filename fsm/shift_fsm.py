from aiogram.fsm.state import State, StatesGroup


class ShiftStates(StatesGroup):
    # Открытие смены
    shift_state = State()
    choose_point = State()
    enter_cash = State()
    confirm_cash = State()
    upload_light_tobacco_photo = State()
    confirm_light_tobacco_photo = State()
    upload_dark_tobacco_photo = State()
    confirm_dark_tobacco_photo = State()
    resume = State()
    working = State()

    # Закрытие смены
    enter_cash_report = State()
    enter_terminal_report = State()
    upload_remaining_light_tobacco = State()
    confirm_remaining_light_tobacco_photo = State()
    upload_remaining_dark_tobacco_photo = State()
    confirm_remaining_dark_tobacco_photo = State()
    extra_information = State()
    confirm_close_shift = State()


class OrderStates(StatesGroup):
    select_payment = State()
    change_price = State()
    choose_menu = State()
    open_order = State()
    pay_order = State()
    close_order = State()
    confirm_price = State()
    enter_custom_price = State()
    enter_comment = State()


# класс заказа

