from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_open_order_keyboard():
    # Клавиатура для открытия и  старта заказа
    start_order = InlineKeyboardButton ( text="Продолжить", callback_data="choose_menu")
    row = [start_order]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard

def get_choose_menu_keyboard():
    medium = InlineKeyboardButton (text= "Медиум", callback_data="position_menu_medium")
    lait = InlineKeyboardButton (text="Лайт", callback_data="position_menu_lait")
    fruit = InlineKeyboardButton (text= "На фрукте", callback_data="position_menu_fruit")
    row = [medium, lait, fruit]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard

def get_payment_keyboard():
    cash = InlineKeyboardButton (text= "Оплата наличными", callback_data="pay_cash")
    card = InlineKeyboardButton (text= "Оплата картой", callback_data="pay_card")
    bonus = InlineKeyboardButton (text = "Бонус ", callback_data="bonus")
    back = InlineKeyboardButton ( text = "Назад", callback_data="choose_menu")
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
