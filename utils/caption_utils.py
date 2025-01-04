def final_info_util(cash_report: float,
                    terminal_report: float,
                    extra_information: str) -> str:
    return f"Рапорт кассы: <b>{cash_report}</b>\n" \
           f"Рапорт терминала: <b>{terminal_report}</b>\n" \
           f"Дополнительная информация <b>{extra_information}</b>\n\n" \
           f"Фотография веса табака загружена.\n\n" \
           f"Подтвердите завершение смены или отмените процесс."
