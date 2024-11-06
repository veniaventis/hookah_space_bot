from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.employe_keyboard import get_point_selection_keyboard, get_shift_management_keyboard
from fsm.shift_fsm import ShiftStates
from aiogram.filters import Command

router = Router()


@router.message(Command("start", prefix="!"))
async def start_command(message: types.Message, state: FSMContext):
    await message.answer("Выберите точку продаж:", reply_markup=get_point_selection_keyboard())
    await state.set_state(ShiftStates.choose_point)


@router.callback_query(F.data == "point_bliski")
@router.callback_query(F.data == "point_aioli")
async def select_point(callback: types.CallbackQuery, state: FSMContext):
    point = "Bliski Wschod" if callback.data == "point_bliski" else "Aioli"
    await state.update_data(point=point)
    await callback.message.edit_text(f"Вы выбрали точку: {point}. Нажмите 'Открыть смену'.",
                                     reply_markup=get_shift_management_keyboard())


@router.callback_query(F.data == "open_shift")
async def open_shift(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите сумму в кассе:")
    await state.set_state(ShiftStates.enter_cash)
