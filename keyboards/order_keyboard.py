from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_open_order_keyboard():
    # Клавиатура для открытия и  старта заказа
    start_order = InlineKeyboardButton ( text="Продолжить", callback_data="choose_menu")
    row = [start_order]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard

def get_choose_menu_keyboard():
    medium = InlineKeyboardButton (text= "Медиум", callback_data="position_menu_medium")
    light = InlineKeyboardButton (text="Лайт", callback_data="position_menu_light")
    fruit = InlineKeyboardButton (text= "На фрукте", callback_data="position_menu_fruit")
    row = [medium, light, fruit]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard

def get_payment_keyboard():
    cash = InlineKeyboardButton (text= "Оплата наличными", callback_data="pay_cash")
    card = InlineKeyboardButton (text= "Оплата картой", callback_data="pay_card")
    bonus = InlineKeyboardButton (text = "Бонус ", callback_data="bonus")
    back = InlineKeyboardButton ( text = " Назад", callback_data="price_option")
    rows = [
           [cash],
           [card],
           [bonus],
           [back]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_close_order_keyboard():
    back = InlineKeyboardButton ( text="Сахранить заказ", callback_data="close_shift")
    che = InlineKeyboardButton ( text="Изминить способ оплаты", callback_data="select_payment")
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
    builder.button(text="Назад", callback_data="choose_menu")
    builder.adjust(1)
    return builder.as_markup()
