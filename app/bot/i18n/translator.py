from locales.en.txt import EN
from locales.ru.txt import RU


def get_translations() -> dict[str, str | dict[str, str]]:
    return {
        "default": "ru",
        "en": EN,
        "ru": RU,
    }
