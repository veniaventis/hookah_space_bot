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


def get_confirmation_keyboard():
    """Клавиатура для подтверждения суммы в кассе."""
    confirm = InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")
    change = InlineKeyboardButton(text="🔄 Изменить ", callback_data="change")
    row = [confirm, change]
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


def get_close_shift_keyboard():
    """Клавиатура для завершения смены."""
    close_shift_btn = InlineKeyboardButton("Завершить смену", callback_data="close_shift")
    cancel_btn = InlineKeyboardButton("Отменить", callback_data="cancel_close_shift")
    row = [close_shift_btn, cancel_btn]
    rows = [row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_change_information_open_shift_keyboard():
    point_of_sale = InlineKeyboardButton(text="🏢 Точка продаж", callback_data="point_of_sale")
    cash_report = InlineKeyboardButton(text="📃 Рапорт кассы", callback_data="cash_report")
    upload_light_tobacco_photo = InlineKeyboardButton(text="🤍 Фото веса светлого табака", callback_data="upload_light_tobacco_photo")
    upload_dark_tobacco_photo = InlineKeyboardButton(text="🖤 Фото веса темного табака", callback_data="upload_dark_tobacco_photo")
    row = [point_of_sale]
    row1 = [cash_report]
    row2 = [upload_light_tobacco_photo]
    row3 = [upload_dark_tobacco_photo]
    rows = [row, row1, row2, row3]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard


def get_changer_information_close_shift():
    cash_report = InlineKeyboardButton(text="📃 Рапорт кассы", callback_data="end_cash_report")
    terminal_report = InlineKeyboardButton(text="📠 Рапорт терминала", callback_data="end_terminal_report")
    upload_light_tobacco_photo = InlineKeyboardButton(text="🤍 Фото остатков светлого табака",
                                                      callback_data="end_upload_light_tobacco_photo")
    upload_dark_tobacco_photo = InlineKeyboardButton(text="🖤 Фото остатков темного табака",
                                                     callback_data="end_upload_dark_tobacco_photo")
    extra_information = InlineKeyboardButton(text="📝 Дополнительная информация",
                                             callback_data="end_extra_information")
    row = [cash_report]
    row1 = [terminal_report]
    row2 = [upload_light_tobacco_photo]
    row3 = [upload_dark_tobacco_photo]
    row4 = [extra_information]
    rows = [row, row1, row2, row3, row4]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard

