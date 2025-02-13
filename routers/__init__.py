__all__ = ("router",)

from aiogram import Router
from .commands import router as commands_router
from .commands.admin_commands import router as admin_commands_router
from .commands.order_commands import router as order_commands_router
from .commands.shift_commands import router as shift_commands_router

router = Router()

router.include_routers(commands_router,
                       admin_commands_router,
                       order_commands_router,
                       shift_commands_router)

#this should be last regestration always
# router.include_router(common_router)
