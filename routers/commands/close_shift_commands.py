from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from db.crud import get_point_name_by_shift_id, get_start_shift_cash, close_shift
from filters.employee_filter import EmployeeFilter
from fsm.shift_fsm import ShiftStates
from keyboards.employe_keyboard import get_confirmation_keyboard, get_photo_confirmation_keyboard
from utils.caption_utils import final_info_util

router = Router()


@router.message(Command("close_shift"), StateFilter(ShiftStates.working),
                EmployeeFilter())
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
    await callback.message.edit_text("Пришлите фотографию оставшегося <b>светлого</b> табака.")
    await state.set_state(ShiftStates.upload_remaining_light_tobacco)


@router.callback_query(StateFilter(ShiftStates.enter_terminal_report), F.data == "change")
async def retry_terminal_report(callback: types.CallbackQuery):
    await callback.message.edit_text("Введите рапорт терминала ещё раз.")


@router.message(StateFilter(ShiftStates.upload_remaining_light_tobacco), F.photo)
async def upload_remaining_tobacco(message: types.Message, state: FSMContext):
    tobacco_photo = message.photo[-1].file_id
    await state.update_data(light_tobacco_photo=tobacco_photo)

    await message.answer_photo(
        photo=tobacco_photo,
        caption="Вы загрузили фотографию веса <b>тёмного</b> табака. Подтвердите что все верно",
        reply_markup=get_photo_confirmation_keyboard()
    )
    await state.set_state(ShiftStates.confirm_remaining_light_tobacco_photo)


@router.callback_query(StateFilter(ShiftStates.confirm_remaining_light_tobacco_photo), F.data == "confirm_photo")
async def confirm_light_tobacco_photo(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Пришлите фотографию веса <b>тёмного</b> табака.", )
    await state.set_state(ShiftStates.upload_remaining_dark_tobacco_photo)


@router.callback_query(StateFilter(ShiftStates.confirm_remaining_light_tobacco_photo), F.data == "change_photo")
async def add_new_photo_light_tobacco(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_caption(
        caption="Загрузите новую фотографию"
    )
    await state.set_state(ShiftStates.upload_remaining_light_tobacco)


@router.message(StateFilter(ShiftStates.upload_remaining_dark_tobacco_photo), F.photo)
async def upload_remaining_dark_tobacco_photo(message: types.Message, state: FSMContext):
    tobacco_photo = message.photo[-1].file_id
    await state.update_data(dark_tobacco_photo=tobacco_photo)

    await message.answer_photo(
        photo=tobacco_photo,
        caption="Вы загрузили фотографию веса <b>тёмного</b> табака. Подтвердите что все верно",
        reply_markup=get_photo_confirmation_keyboard()
    )
    await state.set_state(ShiftStates.confirm_remaining_dark_tobacco_photo)


@router.callback_query(StateFilter(ShiftStates.confirm_remaining_dark_tobacco_photo), F.data == "confirm_photo")
async def confirm_dark_tobacco_photo(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Введите дополнительную информацию о смене.\n<i>(Например количество углей, количество фруктов)</i>"
    )
    await state.set_state(ShiftStates.extra_information)


@router.callback_query(StateFilter(ShiftStates.confirm_remaining_dark_tobacco_photo), F.data == "change_photo")
async def add_new_photo_dark_tobacco(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_caption(
        caption="Загрузите новую фотографию"
    )
    await state.set_state(ShiftStates.upload_remaining_dark_tobacco_photo)


@router.message(StateFilter(ShiftStates.extra_information))
async def final_info(message: types.Message, state: FSMContext):
    # Подготовка данных для финального подтверждения
    await state.update_data(extra_information=message.text)
    data = await state.get_data()
    cash_report = data.get("cash_report")
    terminal_report = data.get("terminal_report")
    light_tobacco_photo = data.get("light_tobacco_photo")
    dark_tobacco_photo = data.get("dark_tobacco_photo")
    extra_information = data.get("extra_information")

    await message.answer_photo(
        photo=light_tobacco_photo,
        caption=(
            "Фото <b>cветлого</b> табака"
        )
    )

    await message.answer_photo(
        photo=dark_tobacco_photo,
        caption=(
            "Фото <b>тёмного</b> табака"
        )
    )

    await message.answer(
        text=(
            final_info_util(cash_report, terminal_report, extra_information)
        ),
        reply_markup=get_confirmation_keyboard()
    )
    await state.set_state(ShiftStates.confirm_close_shift)


@router.callback_query(StateFilter(ShiftStates.confirm_close_shift), F.data == "confirm")
async def finish_shift(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # Сохраняем данные в базу или журнал (пример).
    point = await get_point_name_by_shift_id(callback.from_user.id)
    start_shift_money = await get_start_shift_cash(callback.from_user.id)
    end_shift_cash_report = data.get("cash_report")
    terminal_report = data.get("terminal_report")
    extra_information = data.get("extra_information")

    print(f"{end_shift_cash_report} ")

    await callback.message.edit_text(
        text=(
            f"Смена на точке <b>{point}</b> завершена.\n\n"
            f"Сумма в кассе на начало смены: <b>{start_shift_money}</b>\n\n"
            f"{final_info_util(end_shift_cash_report, terminal_report, extra_information)}\n\n"
            "Все данные успешно сохранены."
        )
    )

    await close_shift(cash_report=end_shift_cash_report,
                      terminal_report=terminal_report,
                      light_tobacco_photo=data.get("light_tobacco_photo"),
                      dark_tobacco_photo=data.get("dark_tobacco_photo"),
                      extra_information=extra_information,
                      employee_id=callback.from_user.id)
    await state.clear()


@router.callback_query(StateFilter(ShiftStates.confirm_close_shift), F.data == "change")
async def cancel_finish_shift(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Завершение смены отменено. Вы можете повторить процесс, используя команду /close_shift",
        reply_markup=None
    )
    await state.set_state(ShiftStates.working)
