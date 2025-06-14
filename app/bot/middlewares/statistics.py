import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update, User
from app.infrastructure.database.db import add_user_activity
from psycopg import AsyncConnection

logger = logging.getLogger(__name__)


class ActivityCounterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        
        user: User = data.get("event_from_user")
        if user is None:
            return await handler(event, data)
        
        result = await handler(event, data)
        
        conn: AsyncConnection = data.get("conn")
        if conn is None:
            logger.error("No database connection found in middleware data.")
            raise RuntimeError("Missing database connection for activity logging.")
        
        await add_user_activity(conn, user_id=user.id)

        return result
