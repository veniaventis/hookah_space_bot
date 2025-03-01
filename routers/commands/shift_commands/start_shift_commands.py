from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.employe_keyboard import get_point_selection_keyboard, get_shift_management_keyboard, \
    get_photo_confirmation_keyboard, get_change_information_open_shift_keyboard
from keyboards.common_keyboard import get_confirmation_keyboard
from fsm.shift_fsm import ShiftStates
from aiogram.filters import Command, StateFilter
from db.crud import create_shift
from filters.employee_filter import EmployeeFilter

router = Router()


@router.message(Command("start_shift"), EmployeeFilter())
async def start_command(message: types.Message, state: FSMContext):
    await message.answer("Выберите точку продаж:", reply_markup=get_point_selection_keyboard())
    await state.set_state(ShiftStates.shift_state)


@router.callback_query(StateFilter(ShiftStates.shift_state), F.data == "point_bliski")
@router.callback_query(StateFilter(ShiftStates.shift_state), F.data == "point_aioli")
async def select_point(callback: types.CallbackQuery, state: FSMContext):
    point = "Bliski Wschod" if callback.data == "point_bliski" else "Aioli"
    await state.update_data(point=point)
    await callback.message.edit_text(
        f"Вы выбрали точку: <b>{point}</b>.\n\nНажмите <i>'Открыть смену'</i>. Или выберите другую точку.",
        reply_markup=get_shift_management_keyboard())
    await state.set_state(ShiftStates.choose_point)


@router.callback_query(F.data == "open_shift")
async def open_shift(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите сумму в кассе:")
    await state.set_state(ShiftStates.enter_cash)


@router.callback_query(StateFilter(ShiftStates.choose_point), F.data == "back")
async def back(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите точку продаж:", reply_markup=get_point_selection_keyboard())
    await state.set_state(ShiftStates.shift_state)


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
    await callback.message.edit_text("Теперь отправьте фотографию веса <b>светлого</b> табака.")
    await state.set_state(ShiftStates.upload_light_tobacco_photo)


@router.callback_query(StateFilter(ShiftStates.confirm_cash), F.data == "change")
async def change_cash(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Пожалуйста, введите корректную сумму в кассе:")
    await state.set_state(ShiftStates.enter_cash)


@router.message(StateFilter(ShiftStates.upload_light_tobacco_photo), F.photo)
async def upload_light_tobacco_photo(message: types.Message, state: FSMContext):
    # Сохраняем ID загруженной фотографии
    light_tobacco_photo = message.photo[-1].file_id
    await state.update_data(light_tobacco_photo=light_tobacco_photo)

    # Отправляем фото для подтверждения
    await message.answer_photo(
        photo=light_tobacco_photo,
        caption="Вы загрузили фотографию веса <b>легкого</b> табака. Подтвердите, что всё верно.",
        reply_markup=get_photo_confirmation_keyboard()
    )
    await state.set_state(ShiftStates.confirm_light_tobacco_photo)


@router.callback_query(StateFilter(ShiftStates.confirm_light_tobacco_photo), F.data == "confirm_photo")
async def confirm_light_tobacco_photo(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Отправьте фотографию веса <b>темного</b> табака.")
    await state.set_state(ShiftStates.upload_dark_tobacco_photo)


@router.callback_query(StateFilter(ShiftStates.confirm_light_tobacco_photo), F.data == "change_photo")
async def change_light_tobacco_photo(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_caption(
        caption="Пожалуйста, загрузите новую фотографию веса табака."
    )
    await state.set_state(ShiftStates.upload_light_tobacco_photo)


@router.message(StateFilter(ShiftStates.upload_dark_tobacco_photo), F.photo)
async def upload_dark_tobacco_photo(message: types.Message, state: FSMContext):
    dark_tobacco_photo = message.photo[-1].file_id
    await state.update_data(dark_tobacco_photo=dark_tobacco_photo)

    await message.answer("Фотография веса темного табака успешно загружена. Подтвердите или измените.")
    await message.answer_photo(
        photo=dark_tobacco_photo,
        caption="Вы загрузили фотографию веса <b>тёмного</b> табака. Подтвердите, что всё верно.",
        reply_markup=get_photo_confirmation_keyboard()
    )
    await state.set_state(ShiftStates.confirm_dark_tobacco_photo)


@router.callback_query(StateFilter(ShiftStates.confirm_dark_tobacco_photo), F.data == "change_photo")
async def confirm_light_tobacco_photo(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_caption(
        caption="Пожалуйста, загрузите новую фотографию веса <b>тёмного</b> табака.")
    await state.set_state(ShiftStates.upload_dark_tobacco_photo)


@router.callback_query(StateFilter(ShiftStates.confirm_dark_tobacco_photo), F.data == "confirm_photo")
async def confirm_photo(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # Получаем фотографии
    light_tobacco_photo = data.get("light_tobacco_photo")
    dark_tobacco_photo = data.get("dark_tobacco_photo")

    # Резюме
    point = data.get("point")
    cash = data.get("cash")

    # Отправка фотографий
    await callback.message.answer_photo(
        photo=light_tobacco_photo,
        caption="<b>Фото легкого табака:</b>"
    )

    await callback.message.answer_photo(
        photo=dark_tobacco_photo,
        caption="<b>Фото темного табака:</b>"
    )

    # Отправляем сообщения с фотографиями и резюме
    await callback.message.answer(
        f"Смена на точке <b>{point}</b>.\n"
        f"Сумма в кассе: <b>{cash}</b>.\n\n"
        f"Подтвердить?",
        reply_markup=get_confirmation_keyboard()
    )

    await state.set_state(ShiftStates.resume)


@router.callback_query(StateFilter(ShiftStates.resume), F.data == "confirm")
async def open_shift(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    # Получаем фотографии

    light_tobacco_photo = data.get("light_tobacco_photo")
    dark_tobacco_photo = data.get("dark_tobacco_photo")

    # Резюме
    point = data.get("point")
    cash = data.get("cash")

    await callback.message.answer(
        f"Смена на точке <b>{point}</b> успешно открыта.\n"
        f"Сумма в кассе: <b>{cash}</b>.\nФотография веса табака сохранена.\n\n"
        f"Хорошего рабочего дня <b>{callback.from_user.full_name}</b>"
    )

    # Завершаем процесс
    await create_shift(
        start_shift_cash=cash,
        tobacco_light_photo_id=light_tobacco_photo,
        tobacco_dark_photo_id=dark_tobacco_photo,
        employee_id=callback.from_user.id,
        point_name=point
    )

    await state.set_state(ShiftStates.working)


@router.callback_query(StateFilter(ShiftStates.resume), F.data == "change")
async def change_information(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выберите место от которого хотите изменить данные",
        reply_markup=get_change_information_open_shift_keyboard()
    )


@router.callback_query(F.data == "point_of_sale")
@router.callback_query(F.data == "cash_report")
@router.callback_query(F.data == "upload_light_tobacco_photo")
@router.callback_query(F.data == "upload_dark_tobacco_photo")
async def change_information(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "point_of_sale":
        await callback.message.answer("Выберите точку продаж:", reply_markup=get_point_selection_keyboard())
        await state.set_state(ShiftStates.choose_point)
    elif callback.data == "cash_report":
        await callback.message.answer("Введите сумму в кассе:")
        await state.set_state(ShiftStates.enter_cash)
    elif callback.data == "upload_light_tobacco_photo":
        await callback.message.edit_text("Отправьте фотографию веса <b>светлого</b> табака.")
        await state.set_state(ShiftStates.upload_light_tobacco_photo)
    elif callback.data == "upload_dark_tobacco_photo":
        await callback.message.edit_text("Отправьте фотографию веса <b>темного</b> табака.")
        await state.set_state(ShiftStates.upload_dark_tobacco_photo)
