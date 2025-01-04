from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я POS бот для <b>Shisha Space</b> .\nДля начала работы введите /start_shift")
