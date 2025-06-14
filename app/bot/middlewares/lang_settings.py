import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Update, User

logger = logging.getLogger(__name__)


class LangSettingsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")
        if user is None:
            return await handler(event, data)
        
        if event.callback_query is None:
            return await handler(event,  data)
        
        locales: list[str] = data.get('locales')

        state: FSMContext = data.get('state')
        user_context_data: dict = await state.get_data()

        if event.callback_query.data == "cancel_lang_button_data":
            user_context_data.update(user_lang=None)
            await state.set_data(user_context_data)

        elif (
            event.callback_query.data in locales 
            and 
            event.callback_query.data != user_context_data.get('user_lang')
        ):
            user_context_data.update(user_lang=event.callback_query.data)
            await state.set_data(user_context_data)

        return await handler(event, data)
