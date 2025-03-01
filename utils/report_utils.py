from db.crud import get_monthly_total_by_payment, get_monthly_report

MONTHS = {
    "january": ("Январь", 1),
    "february": ("Февраль", 2),
    "march": ("Март", 3),
    "april": ("Апрель", 4),
    "may": ("Май", 5),
    "june": ("Июнь", 6),
    "july": ("Июль", 7),
    "august": ("Август", 8),
    "september": ("Сентябрь", 9),
    "october": ("Октябрь", 10),
    "november": ("Ноябрь", 11),
    "december": ("Декабрь", 12),
}


async def get_monthly_report_by_month(month: int):
    monthly_report = await get_monthly_report(month)
    monthly_report_by_cash = await get_monthly_total_by_payment(month, "cash")
    monthly_report_by_card = await get_monthly_total_by_payment(month, "card")
    return monthly_report, monthly_report_by_cash, monthly_report_by_card
