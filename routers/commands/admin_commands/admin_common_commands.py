from aiogram import F, types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.admin_keyboards.admin_keyboard import admin_keyboard

from fsm.admin_fsm import AdminStates

from access.admin_access import admin_list

router = Router()


@router.message(Command("admin", prefix="."), F.from_user.id.in_(admin_list))
async def hello_admin(message: types.Message, state: FSMContext):
    await message.reply(f"Привет, <b>{message.from_user.full_name}</b>!", reply_markup=admin_keyboard())
    await state.set_state(AdminStates.admin_state)



