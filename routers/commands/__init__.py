__all__ = ("router",)

from aiogram import Router
from .admin_commands import router as admin_commands_router
from .shift_commands import router as employe_commands_router
from .start_commands import router as start_commands_router

router = Router()

router.include_routers(start_commands_router,
                       employe_commands_router,
                       admin_commands_router)