from aiogram.filters import BaseFilter
from aiogram.types import Message
from db.crud import load_employee


class EmployeeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        employee_ids = await load_employee()
        return message.from_user.id in employee_ids
