from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import FSInputFile
from fsm.admin_fsm import ReportsStates, AdminStates
from keyboards.admin_keyboards.admin_report_keyboard import *
from keyboards.admin_keyboards.admin_keyboard import admin_keyboard
from keyboards.common_keyboard import get_confirmation_keyboard

from utils.report_utils import get_monthly_report_by_month, MONTHS
from utils.caption_utils import report_captions
from utils.file_utils import export_monthly_report

router = Router()


@router.callback_query(F.data == "report")
async def monthly_report(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите тип отчета", reply_markup=get_report_menu_keyboard())
    await state.set_state(ReportsStates.select_report_type)


@router.callback_query(StateFilter(ReportsStates.select_report_type), F.data == "back")
async def back_to_admin_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.admin_state)
    await callback.message.answer("Меню администратора", reply_markup=admin_keyboard())
    await callback.message.delete_reply_markup()


@router.callback_query(StateFilter(ReportsStates.select_report_type), F.data == "monthly_report")
async def monthly_report(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите месяц, за который хотите получить отчет",
                                  reply_markup=get_monthly_report_keyboard())
    await state.set_state(ReportsStates.monthly_report)


@router.callback_query(StateFilter(ReportsStates.monthly_report), F.data == "back")
async def back_to_report_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите тип отчета", reply_markup=get_report_menu_keyboard())
    await callback.message.delete_reply_markup()
    await state.set_state(ReportsStates.select_report_type)


@router.callback_query(StateFilter(ReportsStates.monthly_report), F.data.in_(MONTHS.keys()))
async def monthly_report_by_month(callback: types.CallbackQuery, state: FSMContext):
    month_name, month_number = MONTHS[callback.data]
    await state.update_data(month_name=month_name, month_number=month_number)
    month_report, month_report_by_cash, month_report_by_card = await get_monthly_report_by_month(month_number)
    await callback.message.answer(f"Отчет за {month_name}.\n{report_captions(month_report,
                                                                             month_report_by_cash,
                                                                             month_report_by_card)}",
                                  reply_markup=get_create_file_keyboard())
    await callback.message.delete_reply_markup()
    await state.set_state(ReportsStates.report_showed)


@router.callback_query(StateFilter(ReportsStates.report_showed), F.data == "back")
async def back_to_monthly_report(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите месяц, за который хотите получить отчет",
                                  reply_markup=get_monthly_report_keyboard())
    await callback.message.delete_reply_markup()
    await state.set_state(ReportsStates.monthly_report)


@router.callback_query(StateFilter(ReportsStates.report_showed), F.data == "create_file")
async def creation_report_file_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Создать файл с отчетом?", reply_markup=get_confirmation_keyboard())
    await state.set_state(ReportsStates.create_report_file)


@router.callback_query(StateFilter(ReportsStates.create_report_file), F.data == "confirm")
async def create_report_file(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    month_number = data.get("month_number")
    month_name = data.get("month_name")
    file_path = f"report_files/Отчет_{month_name}.xlsx"
    document = FSInputFile(file_path)
    await export_monthly_report(month_number, file_path)
    await callback.message.answer_document(document=document, caption="Отчет за месяц")
