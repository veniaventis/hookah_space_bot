from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    admin_state = State()
    staff_menu = State()


class ReportsStates(StatesGroup):
    select_report_type = State()
    monthly_report = State()
    report_showed = State()
    create_report_file = State()


class MonthStates(StatesGroup):
    january = State()
    february = State()
    march = State()
    april = State()
    may = State()
    june = State()
    july = State()
    august = State()
    september = State()
    october = State()
    november = State()
    december = State()


class AddEmployee(StatesGroup):
    waiting_for_employee_id = State()
    waiting_for_employee_name = State()
