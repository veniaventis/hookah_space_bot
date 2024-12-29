from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_keyboard():
    add_employee = InlineKeyboardButton(text="Добавить сотрудника", callback_data="add_employee")
    delete_employee = InlineKeyboardButton(text="Удалить сотрудника", callback_data="delete_employee")
    add_point = InlineKeyboardButton(text="Добавить точку продаж", callback_data="add_point")
    delete_point = InlineKeyboardButton(text="Удалить точку продаж", callback_data="delete_point")
    rows = [
        [add_employee],
        [delete_employee],
        [add_point],
        [delete_point]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard
