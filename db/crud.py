from datetime import datetime

from sqlalchemy import select, update
from db.models.models import Shift, PointOfSale
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
async def create_shift(session, start_shift_cash: float, tobacco_photo_id: str, employee_id: int,
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
                      start_shift_tobacco_photo_id=tobacco_photo_id)
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
        tobacco_photo: str,
        extra_information: str,
        employee_id: int,
):
    active_shift = await get_active_shift(employee_id)
    query = update(Shift).where(Shift.id == active_shift.id).values(
        end_shift_cash=cash_report,
        end_shift_terminal_report=terminal_report,
        end_shift_tobacco_photo_id=tobacco_photo,
        extra_information=extra_information,
        close_datetime=datetime.now()
    )
    await session.execute(query)
    await session.commit()
