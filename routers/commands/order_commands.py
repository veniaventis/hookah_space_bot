from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from keyboards.order_keyboard import (
    get_open_order_keyboard,
    get_choose_menu_keyboard,
    get_payment_keyboard,
    get_close_order_keyboard,
    get_price_option_keyboard,
    get_payment_keyboard_back
)
from fsm.shift_fsm import ShiftStates, OrderStates

router = Router()

@router.message(Command("order"), StateFilter(ShiftStates.working), F.from_user.id.in_({5477880310, 1614891721}))
async def order_command(message: types.Message, state: FSMContext):
    # Если смена открыта, продолжаем выполнение
    await message.answer("Заказ открыт:", reply_markup=get_open_order_keyboard())
    await state.set_state(OrderStates.choose_menu)

@router.callback_query(F.data == "choose_menu")
async def continue_order(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите тип кальяна:", reply_markup=get_choose_menu_keyboard())
    await state.set_state(OrderStates.choose_menu)

@router.callback_query( StateFilter(OrderStates.choose_menu))
async def select_hookah(callback: types.CallbackQuery, state: FSMContext):
    hookah_prices = {
        "position_menu_medium": {"name": "Медиум", "price": 150},
        "position_menu_light": {"name": "Лайт", "price": 100},
        "position_menu_fruit": {"name": "На фрукте", "price": 200}
    }
    selected_data = hookah_prices[callback.data]
    await state.update_data(hookah=selected_data["name"], price=selected_data["price"])

    await callback.message.edit_text(
        f"Вы выбрали: {selected_data['name']}.\n"
        f"Стандартная стоимость: {selected_data['price']} zł.\n"
        f"Хотите оставить цену по умолчанию или изменить?",
        reply_markup=get_price_option_keyboard()
    )
    await state.set_state(OrderStates.confirm_price)

@router.callback_query (F.data== "pop")
async def pop_to_choose_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text (text="Выберите кальян", reply_markup=get_choose_menu_keyboard())
    await state.set_state(OrderStates.choose_menu)


@router.callback_query(F.data == "leave_price", StateFilter(OrderStates.confirm_price))
async def leave_price(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    hookah = data.get("hookah")
    price = data.get("price")
    await callback.message.edit_text(
        f"Вы выбрали: {hookah}. Стоимость: {price} zł.\nВыберите способ оплаты:",
        reply_markup=get_payment_keyboard()
    )
    await state.set_state(OrderStates.pay_order)

@router.callback_query (F.data=="go_back")
async def back_to_pay_order(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text (text="Хочешь изменить цену?", reply_markup=get_price_option_keyboard())
    await state.set_state(OrderStates.confirm_price)

@router.callback_query(F.data == "change_price", StateFilter(OrderStates.confirm_price))
async def ask_custom_price(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите новую цену (только число):")
    await state.set_state(OrderStates.enter_custom_price)

@router.message(StateFilter(OrderStates.enter_custom_price))
async def enter_custom_price(message: types.Message, state: FSMContext):
    try:
        custom_price = float(message.text)
        a= -1
        if custom_price <= a:
            raise ValueError("Цена должна быть положительной.")
        await state.update_data(price=custom_price)
        await message.answer("Комментарий изменения цены :")
        await state.set_state(OrderStates.enter_comment)
    except ValueError:
        await message.answer("Ошибка: введите положительное число, например 150 или 200.")

@router.message(StateFilter(OrderStates.enter_comment))
async def enter_comment(message: types.Message, state: FSMContext):
    comment = message.text
    data = await state.get_data()
    hookah = data.get("hookah")
    price = data.get("price")

    await state.update_data(comment=comment)
    await message.answer(
        f"Вы выбрали: {hookah}.\n"
        f"Новая стоимость: {price} zł.\n"
        f"Комментарий: {comment}.\n"
        f"Выберите способ оплаты:",
        reply_markup=get_payment_keyboard()
    )
    await state.set_state(OrderStates.pay_order)

@router.callback_query(F.data.in_({"pay_cash", "pay_card", "bonus"}), StateFilter(OrderStates.pay_order))
async def select_payment(callback: types.CallbackQuery, state: FSMContext):
    payment_methods = {
        "pay_cash": "наличными",
        "pay_card": "картой",
        "bonus": "бонусом"
    }
    payment_method = payment_methods[callback.data]
    await state.update_data(payment=payment_method)

    data = await state.get_data()
    order_info = (
        f"Заказ:\n"
        f"- Тип кальяна: {data['hookah']}\n"
        f"- Стоимость: {data['price']} zł\n"
        f"- Комментарий: {data.get('comment', 'нет')}\n"
        f"- Способ оплаты: {payment_method}\n"
    )
    await callback.message.edit_text(
        f"{order_info}\nНажмите 'Закрыть заказ', чтобы завершить.",
        reply_markup=get_close_order_keyboard()
   )
    await state.set_state(OrderStates.close_order)

@router.callback_query (F.data=="change_payment")
async def back_change_payment(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text (text="Изменить спомоб оплаты", reply_markup=get_payment_keyboard_back())
    await state.set_state(OrderStates.pay_order)


@router.callback_query (F.data=="close_order")
async def close_order(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Заказ принят и закрыт. спасибо",
        reply_markup=None
    )
    await state.set_state(ShiftStates.working)