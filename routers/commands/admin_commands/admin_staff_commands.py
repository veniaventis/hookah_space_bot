from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from db.crud import get_employee_by_id, create_employee
from fsm.admin_fsm import AddEmployee, AdminStates

from keyboards.admin_keyboards.admin_staff_keyboard import manage_employee_keyboard
from keyboards.admin_keyboards.admin_keyboard import admin_keyboard

router = Router()


@router.callback_query(F.data == "staff")
async def staff_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Меню управления штатом", reply_markup=manage_employee_keyboard())
    await state.set_state(AdminStates.staff_menu)


@router.callback_query(StateFilter(AdminStates.admin_state), F.data == "back")
async def back(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f"Привет <b>{callback.from_user.full_name}</b>", reply_markup=admin_keyboard())
    await state.set_state(AdminStates.admin_state)


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
