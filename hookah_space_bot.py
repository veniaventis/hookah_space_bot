import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN
from db.base import create_tables
from db.crud import initialize_points_of_sale
from routers import router as main_router


async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(main_router)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # await create_tables()
    await initialize_points_of_sale()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
