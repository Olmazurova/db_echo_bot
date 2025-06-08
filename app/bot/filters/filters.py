from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from psycopg import AsyncConnection

from app.bot.enums.roles import UserRole
from app.infrastructure.database.db import get_user_role


class LocaleFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery, locales: list):
        if not isinstance(callback, CallbackQuery):
            raise ValueError(
                f"LocaleFilter: expected `CallbackQuery`, got `{type(callback).__name__}`"
            )
        return callback.data in locales


class UserRoleFilter(BaseFilter):
    def __init__(self, *roles: str | UserRole):
        if not roles:
            raise ValueError(
                "At least one role must be provided to UserRoleFilter.")

        self.roles = frozenset(
            UserRole(role) if isinstance(role, str) else role
            for role in roles
            if isinstance(role, (str, UserRole))
        )

        if not self.roles:
            raise ValueError("No valid roles provided to `UserRoleFilter`.")

    async def __call__(self, event: Message | CallbackQuery,
                       conn: AsyncConnection) -> bool:
        user = event.from_user
        if not user:
            return False

        role = await get_user_role(conn, user_id=user.id)
        if role is None:
            return False

        return role in self.roles
