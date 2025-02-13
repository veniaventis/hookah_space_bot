__all__ = ("router",)

from aiogram import Router

from .start_shift_commands import router as start_shift_commands_router
from .close_shift_commands import router as close_shift_commands_router

router = Router()

router.include_routers(start_shift_commands_router,
                       close_shift_commands_router)