__all__ = ("router",)

from aiogram import Router

from .start_commands import router as start_commands_router

router = Router()

router.include_routers(start_commands_router)