from datetime import datetime

from sqlalchemy import select, update
from db.models.models import Shift, PointOfSale, Order, Employee
from .base import connection


@connection
async def initialize_points_of_sale(session):
    # Проверяем, есть ли уже точки продаж в базе
    query = select(PointOfSale)
    result = await session.execute(query)
    existing_points = result.scalars().all()

    # Если таблица пуста, добавляем точки
    if not existing_points:
        points = [
            PointOfSale(name="Bliski Wschod"),
            PointOfSale(name="Aioli")
        ]
        session.add_all(points)
        await session.commit()
        print("Точки продаж успешно добавлены.")
    else:
        print("Точки продаж уже существуют в базе данных.")


@connection
async def get_point_id_by_name(session, point_name):
    query = select(PointOfSale.id).where(PointOfSale.name == point_name)
    result = await session.execute(query)
    return result.scalar()


@connection
async def create_shift(session, start_shift_cash: float, tobacco_light_photo_id: str, tobacco_dark_photo_id: str,
                       employee_id: int,
                       point_name: str):
    point_id = await get_point_id_by_name(point_name)
    if not point_id:
        raise ValueError(f"Точка продаж '{point_name}' не найдена в базе данных.")
    print(point_id)
    new_shift = Shift(employee_id=employee_id,
                      point_id=point_id,
                      open_datetime=datetime.now(),
                      point=point_name,
                      start_shift_cash=start_shift_cash,
                      start_shift_light_tobacco_photo_id=tobacco_light_photo_id,
                      start_shift_dark_tobacco_photo_id=tobacco_dark_photo_id)
    session.add(new_shift)
    await session.commit()
    return new_shift


@connection
async def get_active_shift(session, employee_id: int):
    query = select(Shift).where(Shift.employee_id == employee_id, Shift.close_datetime == None)
    result = await session.execute(query)
    return result.scalars().first()


@connection
async def get_point_name_by_shift_id(session, employee_id: int):
    active_shift = await get_active_shift(employee_id)

    if active_shift is None:
        return None

    query = select(Shift.point).where(Shift.id == active_shift.id)
    result = await session.execute(query)
    return result.scalar()


@connection
async def get_start_shift_cash(session, employee_id: int):
    active_shift = await get_active_shift(employee_id)
    query = select(Shift.start_shift_cash).where(Shift.id == active_shift.id)
    result = await session.execute(query)
    return result.scalar()


@connection
async def close_shift(
        session,
        cash_report: float,
        terminal_report: float,
        light_tobacco_photo: str,
        dark_tobacco_photo: str,
        extra_information: str,
        employee_id: int,
):
    active_shift = await get_active_shift(employee_id)
    query = update(Shift).where(Shift.id == active_shift.id).values(
        end_shift_cash=cash_report,
        end_shift_terminal_report=terminal_report,
        end_shift_light_tobacco_photo_id=light_tobacco_photo,
        end_shift_dark_tobacco_photo_id=dark_tobacco_photo,
        extra_information=extra_information,
        close_datetime=datetime.now()
    )
    await session.execute(query)
    await session.commit()


@connection
async def load_employee(session):
    query = select(Employee.id).distinct()
    result = await session.execute(query)
    employees_id = result.scalars().all()
    return employees_id


@connection
async def get_employee_by_id(session, employee_id: int):
    query = select(Employee).where(Employee.id == employee_id)
    result = await session.execute(query)
    return result.scalar()


@connection
async def create_employee(session, employee_id: int, employee_name: str):
    existing_employee = await load_employee()
    if employee_id in existing_employee:
        raise ValueError(f"Сотрудник с id {employee_id} уже существует в базе данных.")
    new_employee = Employee(id=employee_id, name=employee_name)
    session.add(new_employee)
    await session.commit()
    await load_employee()
    return new_employee


@connection
async def create_order(session, shift_id: int, hookah_type: str, price: float, payment_method: str,
                       comment: str = None):
    new_order = Order(
        shift_id=shift_id,
        hookah_type=hookah_type,
        price=price,
        payment_method=payment_method,
        comment=comment
    )
    session.add(new_order)
    await session.commit()
    return new_order


@connection
async def get_orders_by_shift(session, shift_id: int):
    query = select(Order).where(Order.shift_id == shift_id)
    result = await session.execute(query)
    return result.scalars().all()
