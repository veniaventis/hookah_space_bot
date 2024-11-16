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
    confirm = InlineKeyboardButton(text="Да, правильно", callback_data="confirm_cash")
    change = InlineKeyboardButton(text="Изменить сумму", callback_data="change_cash")
    row = [confirm, change]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard
