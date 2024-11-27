from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.employe_keyboard import get_point_selection_keyboard, get_shift_management_keyboard, \
    get_confirmation_keyboard, get_photo_confirmation_keyboard
from fsm.shift_fsm import ShiftStates
from aiogram.filters import Command, StateFilter

router = Router()


@router.message(Command("start_shift"), F.from_user.id.in_({5477880310,1614891721}))
async def start_command(message: types.Message, state: FSMContext):
    await message.answer("Выберите точку продаж:", reply_markup=get_point_selection_keyboard())
    await state.set_state(ShiftStates.choose_point)


@router.callback_query(F.data == "point_bliski")
@router.callback_query(F.data == "point_aioli")
async def select_point(callback: types.CallbackQuery, state: FSMContext):
    point = "Bliski Wschod" if callback.data == "point_bliski" else "Aioli"
    await state.update_data(point=point)
    await callback.message.edit_text(
        f"Вы выбрали точку: <b>{point}</b>.\n\nНажмите <i>'Открыть смену'</i>. Или выберите другую точку.",
        reply_markup=get_shift_management_keyboard())


@router.callback_query(F.data == "open_shift")
async def open_shift(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите сумму в кассе:")
    await state.set_state(ShiftStates.enter_cash)


@router.callback_query(F.data == "back")
async def back(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите точку продаж:", reply_markup=get_point_selection_keyboard())
    await state.set_state(ShiftStates.choose_point)


@router.message(StateFilter(ShiftStates.enter_cash))
async def enter_cash(message: types.Message, state: FSMContext):
    try:
        cash = float(message.text)
        await state.update_data(cash=cash)
        await message.answer(
            f"Вы ввели сумму: <b>{cash}</b>.\nПодтвердите введенные данные.",
            reply_markup=get_confirmation_keyboard()
        )
        await state.set_state(ShiftStates.confirm_cash)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число для суммы в кассе.")


@router.callback_query(StateFilter(ShiftStates.confirm_cash), F.data == "confirm")
async def confirm_cash(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Теперь отправте фотографию веса табака.")
    await state.set_state(ShiftStates.upload_tobacco_photo)


@router.callback_query(StateFilter(ShiftStates.confirm_cash), F.data == "change")
async def change_cash(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Пожалуйста, введите корректную сумму в кассе:")
    await state.set_state(ShiftStates.enter_cash)


@router.message(StateFilter(ShiftStates.upload_tobacco_photo), F.photo)
async def upload_tobacco_photo(message: types.Message, state: FSMContext):
    # Сохраняем ID загруженной фотографии
    tobacco_photo = message.photo[-1].file_id
    await state.update_data(tobacco_photo=tobacco_photo)

    # Отправляем фото для подтверждения
    await message.answer_photo(
        photo=tobacco_photo,
        caption="Вы загрузили фотографию веса табака. Подтвердите, что всё верно.",
        reply_markup=get_photo_confirmation_keyboard()
    )
    await state.set_state(ShiftStates.confirm_tobacco_photo)


@router.callback_query(StateFilter(ShiftStates.confirm_tobacco_photo), F.data == "confirm_photo")
async def confirm_photo(callback: types.CallbackQuery, state: FSMContext):
    # Получаем данные и завершаем процесс
    data = await state.get_data()
    point = data.get("point")
    cash = data.get("cash")

    await callback.message.edit_caption(
        caption=(
            f"Смена на точке <b>{point}</b> успешно открыта.\n"
            f"Сумма в кассе: <b>{cash}</b>.\nФотография веса табака сохранена.\n\n"
            f"Хорошего рабочего дня! 😊"
        )
    )
    await state.set_state(ShiftStates.working)


@router.callback_query(StateFilter(ShiftStates.confirm_tobacco_photo), F.data == "change_photo")
async def change_photo(callback: types.CallbackQuery, state: FSMContext):
    # Уведомляем пользователя о необходимости повторной загрузки фото
    await callback.message.edit_caption(
        caption="Пожалуйста, загрузите новую фотографию веса табака.",
    )
    await state.set_state(ShiftStates.upload_tobacco_photo)


@router.message(Command("close_shift"), F.from_user.id.in_({5477880310, 1614891721}), StateFilter(ShiftStates.working))
async def close_shift_start(message: types.Message, state: FSMContext):
    await message.reply("Введите раппорт кассы (сумма в кассе):")
    await state.set_state(ShiftStates.enter_cash_report)


@router.message(StateFilter(ShiftStates.enter_cash_report))
async def enter_cash_report(message: types.Message, state: FSMContext):
    try:
        cash_report = float(message.text)
        await state.update_data(cash_report=cash_report)
        await message.answer(
            f"Вы ввели рапорт кассы: <b>{cash_report}</b>. Подтвердите или измените.",
            reply_markup=get_confirmation_keyboard()
        )
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")


@router.callback_query(StateFilter(ShiftStates.enter_cash_report), F.data == "confirm")
async def confirm_cash_report(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Теперь введите рапорт терминала.")
    await state.set_state(ShiftStates.enter_terminal_report)


@router.callback_query(StateFilter(ShiftStates.enter_cash_report), F.data == "change")
async def retry_cash_report(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите рапорт кассы ещё раз.")
    await state.set_state(ShiftStates.enter_cash_report)


@router.message(StateFilter(ShiftStates.enter_terminal_report))
async def enter_terminal_report(message: types.Message, state: FSMContext):
    try:
        terminal_report = float(message.text)
        await state.update_data(terminal_report=terminal_report)
        await message.answer(
            f"Вы ввели рапорт терминала: <b>{terminal_report}</b>. Подтвердите или измените.",
            reply_markup=get_confirmation_keyboard()
        )
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")


@router.callback_query(StateFilter(ShiftStates.enter_terminal_report), F.data == "confirm")
async def confirm_terminal_report(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Загрузите фотографию остатка табака.")
    await state.set_state(ShiftStates.upload_remaining_tobacco)


@router.callback_query(StateFilter(ShiftStates.enter_terminal_report), F.data == "change")
async def retry_terminal_report(callback: types.CallbackQuery):
    await callback.message.edit_text("Введите рапорт терминала ещё раз.")


@router.message(StateFilter(ShiftStates.upload_remaining_tobacco), F.photo)
async def upload_remaining_tobacco(message: types.Message, state: FSMContext):
    tobacco_photo = message.photo[-1].file_id
    await state.update_data(tobacco_photo=tobacco_photo)

    # Подготовка данных для финального подтверждения
    data = await state.get_data()
    cash_report = data.get("cash_report")
    terminal_report = data.get("terminal_report")

    await message.answer_photo(
        photo=tobacco_photo,
        caption=(
            f"Рапорт кассы: <b>{cash_report}</b>\n"
            f"Рапорт терминала: <b>{terminal_report}</b>\n"
            f"Фотография веса табака загружена.\n\n"
            "Подтвердите завершение смены или отмените процесс."
        ),
        reply_markup=get_confirmation_keyboard()
    )
    await state.set_state(ShiftStates.confirm_close_shift)


@router.callback_query(StateFilter(ShiftStates.confirm_close_shift), F.data == "confirm")
async def finish_shift(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # Сохраняем данные в базу или журнал (пример).
    point = data.get("point")
    cash_report = data.get("cash_report")
    terminal_report = data.get("terminal_report")
    tobacco_photo = data.get("tobacco_photo")

    await callback.message.edit_caption(
        caption=(
            f"Смена на точке <b>{point}</b> завершена.\n"
            f"Рапорт кассы: <b>{cash_report}</b>\n"
            f"Рапорт терминала: <b>{terminal_report}</b>\n\n"
            "Все данные успешно сохранены."
        ),
        parse_mode="HTML",
        reply_markup=None
    )
    await state.clear()


@router.callback_query(StateFilter(ShiftStates.confirm_close_shift), F.data == "change")
async def cancel_finish_shift(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_caption(
        "Завершение смены отменено. Вы можете повторить процесс",
        reply_markup=None
    )
    await state.set_state(ShiftStates.working)