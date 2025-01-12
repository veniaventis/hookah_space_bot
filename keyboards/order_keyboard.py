from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_open_order_keyboard():
    # Клавиатура для открытия и старта заказа
    start_order = InlineKeyboardButton(text="Продолжить", callback_data="choose_menu")
    row = [start_order]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_choose_menu_keyboard():
    medium = InlineKeyboardButton(text="Medium", callback_data="position_menu_medium")
    light = InlineKeyboardButton(text="Light", callback_data="position_menu_light")
    fruit = InlineKeyboardButton(text="Fruit", callback_data="position_menu_fruit")
    future_fruit = InlineKeyboardButton(text="Future Fruit", callback_data="position_menu_future_fruit")
    row = [light, fruit]
    row1 = [medium, future_fruit]
    rows = [row, row1]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_payment_keyboard():
    cash = InlineKeyboardButton(text="Оплата наличными", callback_data="pay_cash")
    card = InlineKeyboardButton(text="Оплата картой", callback_data="pay_card")
    bonus = InlineKeyboardButton(text="Бонус ", callback_data="bonus")
    back = InlineKeyboardButton(text=" Назад", callback_data="go_back")
    rows = [
        [cash],
        [card],
        [bonus],
        [back]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_payment_keyboard_back():
    cash = InlineKeyboardButton(text="Оплата наличными", callback_data="pay_cash")
    card = InlineKeyboardButton(text="Оплата картой", callback_data="pay_card")
    bonus = InlineKeyboardButton(text="Бонус ", callback_data="bonus")
    rows = [
        [cash],
        [card],
        [bonus]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_close_order_keyboard():
    back = InlineKeyboardButton(text="Сoхранить заказ", callback_data="close_order")
    che = InlineKeyboardButton(text="Измeнить способ оплаты", callback_data="change_payment")
    rows = [
        [back],
        [che]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_price_option_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Оставить цену", callback_data="leave_price")
    builder.button(text="Изменить цену", callback_data="change_price")
    builder.button(text="Назад", callback_data="back_to")
    builder.adjust(1)
    return builder.as_markup()
