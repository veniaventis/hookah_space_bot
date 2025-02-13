__all__ = ("router",)

from aiogram import Router

from .order_commands import router as order_commands_router

router = Router()

router.include_routers(order_commands_router)