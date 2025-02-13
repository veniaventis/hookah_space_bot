__all__ = ("router",)

from aiogram import Router
from .admin_common_commands import router as admin_common_commands_router
from .admin_report_commands import router as admin_report_commands_router
from .admin_staff_commands import router as admin_staff_commands_router

router = Router()

router.include_routers(admin_common_commands_router,
                       admin_report_commands_router,
                       admin_staff_commands_router)



