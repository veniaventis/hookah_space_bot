import pandas as pd
from datetime import datetime
from db.crud import get_shifts_by_month, get_shift_summary, get_orders_by_shift, get_monthly_summary


async def export_monthly_report(month: int, file_path: str = None):
    """Генерирует Excel-файл с отчетом за месяц"""

    # 1️⃣ Получаем все смены за месяц
    shifts = await get_shifts_by_month(month)

    if not shifts:
        print(f"❌ Нет смен за {month}-й месяц!")
        return None

    # 2️⃣ Собираем данные по каждой смене
    data = []
    for shift in shifts:
        summary = await get_shift_summary(shift.id)
        data.append([
            shift.id,
            shift.open_datetime.strftime("%Y-%m-%d %H:%M"),
            shift.close_datetime.strftime("%Y-%m-%d %H:%M") if shift.close_datetime else "Открыта",
            shift.point,
            shift.employee_id,
            summary["orders_count"],
            summary["cash_revenue"],
            summary["card_revenue"],
            summary["cash_revenue"] + summary["card_revenue"]
        ])

    # 3️⃣ Общая статистика за месяц
    monthly_summary = await get_monthly_summary(month)

    # 4️⃣ Создаем DataFrame для смен
    df_shifts = pd.DataFrame(data, columns=[
        "ID смены", "Начало смены", "Конец смены", "Точка продаж", "Сотрудник",
        "Кол-во заказов", "Выручка (наличные)", "Выручка (карта)", "Общая выручка"
    ])

    # 5️⃣ Создаем Excel-файл
    file_name = file_path or f"Отчет_{month}_{datetime.now().year}.xlsx"
    with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
        # Записываем общий отчет по сменам
        df_shifts.to_excel(writer, sheet_name="Отчет по сменам", index=False)

        # 6️⃣ Добавляем детальные заказы по каждой смене
        for shift in shifts:
            orders = await get_orders_by_shift(shift.id)
            if orders:
                df_orders = pd.DataFrame([
                    [o.id, o.hookah_type, o.price, o.payment_method, o.comment]
                    for o in orders
                ], columns=["ID заказа", "Тип кальяна", "Цена", "Метод оплаты", "Комментарий"])
                df_orders.to_excel(writer, sheet_name=f"Смена {shift.id}", index=False)

        # 7️⃣ Записываем общие итоги
        summary_df = pd.DataFrame([
            ["Выручка (наличные)", monthly_summary["total_cash"]],
            ["Выручка (карта)", monthly_summary["total_card"]]
        ], columns=["Показатель", "Значение"])
        summary_df.to_excel(writer, sheet_name="Итоги месяца", index=False)

    print(f"✅ Отчет сохранен: {file_name}")
    return file_name
