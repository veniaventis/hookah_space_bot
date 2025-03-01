from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_keyboard():
    staff_button = InlineKeyboardButton(text="Штат", callback_data="staff")
    report_keyboard = InlineKeyboardButton(text="Отчёты", callback_data="report")
    row = [staff_button, report_keyboard]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard
