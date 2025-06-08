from aiogram.types import BotCommand
from app.bot.enums.roles import UserRole


def get_main_menu_commands(i18n: dict[str, str], role: UserRole):
    if role == UserRole.USER:
        return [
            BotCommand(
                command='/start',
                description=i18n.get('/start_description')
            ),
            BotCommand(
                command='/lang',
                description=i18n.get('/lang_description')
            ),
            BotCommand(
                command='/help',
                description=i18n.get('/help_description')
            ),
        ]
    elif role == UserRole.ADMIN:
        return [
            BotCommand(
                command='/start',
                description=i18n.get('/start_description')
            ),
            BotCommand(
                command='/lang',
                description=i18n.get('/lang_description')
            ),
            BotCommand(
                command='/help',
                description=i18n.get('/help_description')
            ),
            BotCommand(
                command='/ban',
                description=i18n.get('/ban_description')
            ),
            BotCommand(
                command='/unban',
                description=i18n.get('/unban_description')
            ),
            BotCommand(
                command='/statistics',
                description=i18n.get('/statistics_description')
            ),
        ]
