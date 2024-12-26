
from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from keyboards.admin_keyboard import admin_keyboard
from aiogram.fsm.context import FSMContext
from db.crud import create_employee
from fsm.shift_fsm import AddEmployee

router = Router()


@router.message(Command("admin", prefix="."), F.from_user.id.in_({5477880310}))
async def hello_admin(message: types.Message):
    await message.reply("Привет, администратор!", reply_markup=admin_keyboard())


@router.callback_query(F.data == "add_employee")
async def add_employee(callback: types.CallbackQuery,state: FSMContext):
    await callback.message.answer("Пришлите id сотрудника.")
    await state.set_state(AddEmployee.waiting_for_employee_id)


@router.message(StateFilter(AddEmployee.waiting_for_employee_id))
async def process_employee_id(message: types.Message, state: FSMContext):
    employee_id = message.text.strip()
    try:
        employee_id = int(employee_id)
        # Получаем id сотрудника
        await message.answer("Пришлите имя сотрудника.")
    except ValueError:
        await message.answer("Пожалуйста, отправьте корректный числовой id.")
    finally:
        await state.set_state(AddEmployee.waiting_for_employee_name)


@router.message(StateFilter(AddEmployee.waiting_for_employee_name))
async def process_employee_name(message: types.Message, state: FSMContext):
    employee_name = message.text.strip()
    data = await state.get_data()
    employee_id = data.get("employee_id")
    await create_employee(employee_id, employee_name)
