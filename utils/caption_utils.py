def final_info_util(cash_report: float,
                    terminal_report: float,
                    extra_information: str) -> str:
    return f"Рапорт кассы: <b>{cash_report}</b>\n" \
           f"Рапорт терминала: <b>{terminal_report}</b>\n" \
           f"Дополнительная информация <b>{extra_information}</b>\n\n" \
           f"Подтвердите завершение смены или отмените процесс."


def report_captions(month_report: int,
                    month_report_by_cash: int,
                    month_report_by_card: int) -> str:
    return f"Сумма продаж: <b>{month_report}</b>\n" \
           f"Итого наличными: <b>{month_report_by_cash}</b>\n" \
           f"Итого картой: <b>{month_report_by_card}</b>\n"
