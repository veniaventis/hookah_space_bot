__all__ = ("router",)

from aiogram import Router
from .admin_commands import router as admin_commands_router
from .start_shift_commands import router as start_shift_commands_router
from .close_shift_commands import router as close_shift_commands_router
from .start_commands import router as start_commands_router
from .order_commands import router as order_commands_router

router = Router()

router.include_routers(start_commands_router,
                       start_shift_commands_router,
                       close_shift_commands_router,
                       admin_commands_router,
                       order_commands_router)
