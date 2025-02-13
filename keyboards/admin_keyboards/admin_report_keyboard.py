from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.common_keyboard import back_button


def get_report_menu_keyboard():
    monthly_report = InlineKeyboardButton(text="Месячный отчёт", callback_data="monthly_report")
    back = back_button()
    # TODO: add daily repotr
    rows = [
        [monthly_report],
        [back]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_monthly_report_keyboard():
    january = InlineKeyboardButton(text="Январь", callback_data="january")
    february = InlineKeyboardButton(text="Февраль", callback_data="february")
    march = InlineKeyboardButton(text="Март", callback_data="march")
    april = InlineKeyboardButton(text="Апрель", callback_data="april")
    may = InlineKeyboardButton(text="Май", callback_data="may")
    june = InlineKeyboardButton(text="Июнь", callback_data="june")
    july = InlineKeyboardButton(text="Июль", callback_data="july")
    august = InlineKeyboardButton(text="Август", callback_data="august")
    september = InlineKeyboardButton(text="Сентябрь", callback_data="september")
    october = InlineKeyboardButton(text="Октябрь", callback_data="october")
    november = InlineKeyboardButton(text="Ноябрь", callback_data="november")
    december = InlineKeyboardButton(text="Декабрь", callback_data="december")
    back = back_button()
    rows = [
        [january, february, march],
        [april, may, june],
        [july, august, september],
        [october, november, december],
        [back]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_create_file_keyboard():
    create_file = InlineKeyboardButton(text="Создать файл", callback_data="create_file")
    back = back_button()
    rows = [
        [create_file],
        [back]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard
