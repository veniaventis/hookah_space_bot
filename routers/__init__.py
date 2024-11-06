__all__ = ("router",)

from aiogram import Router
from .commands import router as commands_router

router = Router()

router.include_routers(commands_router)

#this should be last regestration always
# router.include_router(common_router)
