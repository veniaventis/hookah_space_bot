from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def back_button():
    return InlineKeyboardButton(text="Назад", callback_data="back")


def get_confirmation_keyboard():
    """Клавиатура для подтверждения суммы в кассе."""
    confirm = InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")
    change = InlineKeyboardButton(text="❌ Отменить", callback_data="change")
    row = [confirm, change]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard
