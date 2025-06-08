import logging

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from app.bot.enums.roles import UserRole
from app.bot.filters.filters import UserRoleFilter
from app.infrastructure.database.db import (
    change_user_banned_status_by_id,
    change_user_banned_status_by_username,
    get_statistics,
    get_user_banned_status_by_id,
    get_user_banned_status_by_username,
)
from psycopg import AsyncConnection

logger = logging.getLogger(__name__)

admin_router = Router()

admin_router.message.filter(UserRoleFilter(UserRole.ADMIN))


# Этот хэндлер будет срабатывать на команду /help для пользователя с ролью `UserRole.ADMIN`
@admin_router.message(Command('help'))
async def process_admin_help_command(message: Message, i18n: dict):
    await message.answer(text=i18n.get('/help_admin'))


# Этот хэндлер будет срабатывать на команду /statistics для пользователя с ролью `UserRole.ADMIN`
@admin_router.message(Command('statistics'))
async def process_admin_statistics_command(message: Message,
                                           conn: AsyncConnection,
                                           i18n: dict[str, str]):
    statistics = await get_statistics(conn)
    await message.answer(
        text=i18n.get("statistics").format(
            "\n".join(
                f"{i}. <b>{stat[0]}</b>: {stat[1]}"
                for i, stat in enumerate(statistics, 1)
            )
        )
    )


# Этот хэндлер будет срабатывать на команду /ban для пользователя с ролью `UserRole.ADMIN`
@admin_router.message(Command("ban"))
async def process_ban_command(
        message: Message,
        command: CommandObject,
        conn: AsyncConnection,
        i18n: dict[str, str]
) -> None:
    args = command.args

    if not args:
        await message.reply(i18n.get('empty_ban_answer'))
        return

    arg_user = args.split()[0].strip()

    if arg_user.isdigit():
        banned_status = await get_user_banned_status_by_id(conn, user_id=int(
            arg_user))
    elif arg_user.startswith('@'):
        banned_status = await get_user_banned_status_by_username(conn,
                                                                 username=arg_user[
                                                                          1:])
    else:
        await message.reply(text=i18n.get('incorrect_ban_arg'))
        return

    if banned_status is None:
        await message.reply(i18n.get('no_user'))
    elif banned_status:
        await message.reply(i18n.get('already_banned'))
    else:
        if arg_user.isdigit():
            await change_user_banned_status_by_id(conn, user_id=int(arg_user),
                                                  banned=True)
        else:
            await change_user_banned_status_by_username(conn,
                                                        username=arg_user[1:],
                                                        banned=True)
        await message.reply(text=i18n.get('succesfully_banned'))


# Этот хэндлер будет срабатывать на команду /unban для пользователя с ролью `UserRole.ADMIN`
@admin_router.message(Command('unban'))
async def process_unban_command(
        message: Message,
        command: CommandObject,
        conn: AsyncConnection,
        i18n: dict[str, str]
) -> None:
    args = command.args

    if not args:
        await message.reply(i18n.get('empty_unban_answer'))
        return

    arg_user = args.split()[0].strip()

    if arg_user.isdigit():
        banned_status = await get_user_banned_status_by_id(conn, user_id=int(
            arg_user))
    elif arg_user.startswith('@'):
        banned_status = await get_user_banned_status_by_username(conn,
                                                                 username=arg_user[
                                                                          1:])
    else:
        await message.reply(text=i18n.get('incorrect_unban_arg'))
        return

    if banned_status is None:
        await message.reply(i18n.get('no_user'))
    elif banned_status:
        if arg_user.isdigit():
            await change_user_banned_status_by_id(conn, user_id=int(arg_user),
                                                  banned=False)
        else:
            await change_user_banned_status_by_username(conn,
                                                        username=arg_user[1:],
                                                        banned=False)
        await message.reply(text=i18n.get('succesfully_unbanned'))
    else:
        await message.reply(i18n.get('not_banned'))
