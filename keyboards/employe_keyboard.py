from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_point_selection_keyboard():
    """Клавиатура для выбора точки продаж."""
    bliski_wschod = InlineKeyboardButton(text="Bliski Wschod 🏜️", callback_data="point_bliski")
    aioli = InlineKeyboardButton(text="Aioli 🌴", callback_data="point_aioli")
    row = [bliski_wschod, aioli]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_shift_management_keyboard():
    """Клавиатура для управления сменой."""
    open_shift_btn = InlineKeyboardButton(text="Открыть смену", callback_data="open_shift")
    back_btn = InlineKeyboardButton(text="Назад", callback_data="back")
    row = [open_shift_btn, back_btn]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard

def get_start_order_keyboard():
    open_start_btn = InlineKeyboardButton(text= "Открыть закз", callback_data="open_start")
    row = [open_start_btn]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard

def get_menu_select_keyboard():
    medium = InlineKeyboardButton(text="Средний", callback_data="position_menu_medium")
    lait = InlineKeyboardButton(text="Легкий", callback_data="position_menu_lait")
    fruit = InlineKeyboardButton(text="На фрукте", callback_data="position_menu_fruit")
    row = [medium, lait , fruit]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard

def get_payment_keyboard():
    cash = InlineKeyboardButton(text ="Оплата Наличными", callback_data="pay_cash")
    card = InlineKeyboardButton(text = "Оплата картой", callback_data="pay_card")
    bonus = InlineKeyboardButton(text= "Бонусный", callback_data="bonus")
    row = [cash,card,bonus]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard

def close_order_keyboard():
    close = InlineKeyboardButton(text = "Закрыть заказ", callback_data="close_order")
    row = [close]
    rows =[row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard

def get_photo_confirmation_keyboard():
    """Клавиатура для подтверждения фотографии."""
    confirmation = InlineKeyboardButton(text="Да, всё верно", callback_data="confirm_photo")
    change = InlineKeyboardButton(text="Загрузить заново", callback_data="change_photo")
    row = [confirmation, change]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_confirmation_keyboard():
    """Клавиатура для подтверждения суммы в кассе."""
    confirm = InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")
    change = InlineKeyboardButton(text="🔄 Изменить ", callback_data="change")
    row = [confirm, change]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_close_shift_keyboard():
    """Клавиатура для завершения смены."""
    close_shift_btn = InlineKeyboardButton("Завершить смену", callback_data="close_shift")
    cancel_btn = InlineKeyboardButton("Отменить", callback_data="cancel_close_shift")
    row = [close_shift_btn,cancel_btn]
    back_btn = InlineKeyboardButton(text="Назад", callback_data="back")
    row = [open_shift_btn, back_btn]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard

def get_photo_confirmation_keyboard():
    """Клавиатура для подтверждения фотографии."""
    confirmation = InlineKeyboardButton(text="Да, всё верно", callback_data="confirm_photo")
    change = InlineKeyboardButton(text="Загрузить заново", callback_data="change_photo")
    row = [confirmation, change]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_confirmation_keyboard():
    """Клавиатура для подтверждения суммы в кассе."""
    confirm = InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")
    change = InlineKeyboardButton(text="🔄 Изменить ", callback_data="change")
    row = [confirm, change]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_close_shift_keyboard():
    """Клавиатура для завершения смены."""
    close_shift_btn = InlineKeyboardButton("Завершить смену", callback_data="close_shift")
    cancel_btn = InlineKeyboardButton("Отменить", callback_data="cancel_close_shift")
    row = [close_shift_btn,cancel_btn]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard

