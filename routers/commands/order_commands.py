from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.order_keyboard import (get_open_order_keyboard, get_choose_menu_keyboard, get_payment_keyboard,
                                      get_close_order_keyboard)
from fsm.shift_fsm import ShiftStates , OrderStates
from aiogram.filters import Command, StateFilter

router = Router()

@router.message(Command("order"), F.from_user.id.in_({5477880310, 1614891721}))
async def order_command(message: types.Message, state: FSMContext):
    data = await state.get_data()  # Получаем все данные FSM
    if not data.get("shift_opened"):  # Проверяем, есть ли флаг и его значение
        await message.answer("Ошибка: сначала откройте смену с помощью команды /start_shift.")
        return

    # Если смена открыта, продолжаем выполнение
    await message.answer("Заказ открыт:", reply_markup=get_open_order_keyboard())
    await state.set_state(OrderStates.choose_menu)

@router.callback_query(F.data == "choose_menu")
async def continue_order(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите тип кальяна:", reply_markup=get_choose_menu_keyboard())
    await state.set_state(OrderStates.choose_menu)  # Сохраняем состояние

@router.callback_query(F.data.in_({"position_menu_medium", "position_menu_lait", "position_menu_fruit"}))
async def select_hookah(callback: types.CallbackQuery, state: FSMContext):
    # Словарь с ценами кальянов
    hookah_prices = {
        "position_menu_medium": {"name": "Медиум", "price": 100},
        "position_menu_lait": {"name": "Лайт", "price": 80},
        "position_menu_fruit": {"name": "На фрукте", "price": 150}
    }

    # Получаем данные о выбранном кальяне
    selected_data = hookah_prices[callback.data]
    await state.update_data(hookah=selected_data["name"], price=selected_data["price"])

    # Переход к оплате
    await callback.message.edit_text(
        f"Вы выбрали: {selected_data['name']}. Стоимость: {selected_data['price']} zł.\nВыберите способ оплаты:",
        reply_markup=get_payment_keyboard()
    )
    await state.set_state(OrderStates.pay_order)

@router.callback_query(F.data.in_({"pay_cash", "pay_card", "bonus"}))
async def select_payment(callback: types.CallbackQuery, state: FSMContext):
    # Получаем выбранный способ оплаты
    payment_methods = {
        "pay_cash": "наличными",
        "pay_card": "картой",
        "bonus": "бонусом"
    }
    payment_method = payment_methods[callback.data]
    await state.update_data(payment=payment_method)

    # Подтверждение выбора и переход к завершению заказа
    data = await state.get_data()
    message_for_admin = (
        f"Заказ:\n"
        f"- Тип кальяна: {data['hookah']}\n"
        f"- Стоимость: {data['price']} zł\n"
        f"- Способ оплаты: {payment_method}\n"
    )
    await callback.message.edit_text(
        f"{message_for_admin}\nНажмите 'Закрыть заказ', чтобы завершить.",
        reply_markup=get_close_order_keyboard()
    )
    await state.set_state(OrderStates.close_order)

@router.callback_query(F.data == "close")
async def close_order(callback: types.CallbackQuery, state: FSMContext):
    # Получение данных текущего заказа
    data = await state.get_data()
    message_for_admin = (
        f"Заказ завершён:\n"
        f"- Тип кальяна: {data['hookah']}\n"
        f"- Стоимость: {data['price']} zł\n"
        f"- Способ оплаты: {data['payment']}\n"
    )

    # Отправка подтверждения админу
    await callback.message.edit_text(
        f"{message_for_admin}\nЗаказ закрыт. Готов к следующему!"
    )

    # Очистка состояния
    await state.clear()
