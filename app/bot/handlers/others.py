from aiogram import Router
from aiogram.types import Message
from psycopg import AsyncConnection

# Инициализируем роутер уровня модуля
others_router = Router()


# Этот хэндлер будет срабатывать на любые апдейты типа `Message`, которые не забрали
# хэндлеры из других роутеров
@others_router.message()
async def send_echo(message: Message, conn: AsyncConnection, i18n: dict):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=i18n.get("no_echo"))
