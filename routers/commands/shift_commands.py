from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.employe_keyboard import get_point_selection_keyboard, get_shift_management_keyboard, \
    get_confirmation_keyboard, get_photo_confirmation_keyboard
from fsm.shift_fsm import ShiftStates
from aiogram.filters import Command, StateFilter

router = Router()


@router.message(Command("start"), F.from_user.id.in_({5477880310}))
async def start_command(message: types.Message, state: FSMContext):
    await message.answer("Выберите точку продаж:", reply_markup=get_point_selection_keyboard())
    await state.set_state(ShiftStates.choose_point)


@router.callback_query(F.data == "point_bliski")
@router.callback_query(F.data == "point_aioli")
async def select_point(callback: types.CallbackQuery, state: FSMContext):
    point = "Bliski Wschod" if callback.data == "point_bliski" else "Aioli"
    await state.update_data(point=point)
    await callback.message.edit_text(f"Вы выбрали точку: <b>{point}</b>.\n\nНажмите <i>'Открыть смену'</i>. Или выберите другую точку.",
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


@router.callback_query(StateFilter(ShiftStates.confirm_cash), F.data == "confirm_cash")
async def confirm_cash(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Теперь отправте фотографию веса табака.")
    await state.set_state(ShiftStates.upload_tobacco_photo)


@router.callback_query(StateFilter(ShiftStates.confirm_cash), F.data == "change_cash")
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
