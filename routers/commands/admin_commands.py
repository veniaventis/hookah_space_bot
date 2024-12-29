from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from keyboards.admin_keyboard import admin_keyboard
from aiogram.fsm.context import FSMContext
from db.crud import create_employee, get_employee_by_id
from fsm.shift_fsm import AddEmployee

from access.admin_access import admin_list

router = Router()


@router.message(Command("admin", prefix="."), F.from_user.id.in_(admin_list))
async def hello_admin(message: types.Message):
    await message.reply("Привет, администратор!", reply_markup=admin_keyboard())


@router.callback_query(F.data == "add_employee")
async def add_employee(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Пришлите <b>ID</b> сотрудника.")
    await state.set_state(AddEmployee.waiting_for_employee_id)


@router.message(StateFilter(AddEmployee.waiting_for_employee_id))
async def process_employee_id(message: types.Message, state: FSMContext):
    employee_id = message.text.strip()
    try:
        employee_id = int(employee_id)
        # Проверяем, существует ли сотрудник с данным ID
        existing_employee = await get_employee_by_id(employee_id)
        if existing_employee:
            await message.answer("Сотрудник с таким <b>ID</b> уже существует. Пожалуйста, введите другой <b>ID</b>.")
            # Снова устанавливаем состояние для ввода ID
            await state.set_state(AddEmployee.waiting_for_employee_id)
            return  # Прерываем выполнение функции
        # Если сотрудник не найден, сохраняем ID и переходим к следующему шагу
        await state.update_data(employee_id=employee_id)
        await message.answer("Пришлите имя сотрудника.")
        await state.set_state(AddEmployee.waiting_for_employee_name)
    except ValueError:
        await message.answer("Пожалуйста, отправьте корректный числовой <b>ID</b>.")
        # Оставляем состояние для повторного ввода ID
        await state.set_state(AddEmployee.waiting_for_employee_id)


@router.message(StateFilter(AddEmployee.waiting_for_employee_name))
async def process_employee_name(message: types.Message, state: FSMContext):
    employee_name = message.text.strip()
    data = await state.get_data()
    employee_id = data.get("employee_id")
    await create_employee(employee_id, employee_name)
    await message.answer(f"Сотрудник"
                         f"\n<b>ID:</b><i>{employee_id}</i>"
                         f"\n<b>Имя</b>:<i>{employee_name}</i>"
                         f"\nуспешно добавлен.")
    await state.clear()


@router.callback_query(F.data == "delete_employee")
async def delete_employee(callback: types.CallbackQuery):
    await callback.message.answer("Функционал в разрaботке.")


@router.callback_query(F.data == "add_point")
async def add_point(callback: types.CallbackQuery):
    await callback.message.answer("Функционал в разрaботке.")


@router.callback_query(F.data == "delete_point")
async def delete_point(callback: types.CallbackQuery):
    await callback.message.answer("Функционал в разрaботке.")
