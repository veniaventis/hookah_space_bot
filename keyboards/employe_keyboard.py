from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_point_selection_keyboard():
    bliski_wschod = InlineKeyboardButton(text="Bliski Wschod", callback_data="point_bliski")
    aioli = InlineKeyboardButton(text="Aioli", callback_data="point_aioli")
    row = [bliski_wschod, aioli]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_shift_management_keyboard():
    open_shift_btn = InlineKeyboardButton(text="Открыть смену", callback_data="open_shift")
    row = [open_shift_btn]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard
