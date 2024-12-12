import access
from aiogram import Router, F, types
from aiogram.filters import Command

router = Router()


@router.message(Command("admin", prefix="."), F.from_user.id.in_({5477880310}))
async def hello_admin(message: types.Message):
    await message.reply("Hello admin")


async def add_employee(message: types.Message):
    pass



dscvsdv
