import re
import datetime


DATE_FORMAT = re.compile(r"(\d{2})\.(\d{2})\.(\d{4})")
ADDRESS_FORMAT = re.compile(r"\w")


def validate_birth_date(birth_date_str: str) -> str:
    """Проверка даты рождения. (datetime.datetime.strptime выдаёт не самые понятные
        сообщения об ошибках для пользователей).
    """
    date_parse = DATE_FORMAT.fullmatch(birth_date_str)
    if not date_parse:
        raise ValueError("Дата рождения должна быть в формате ДД.ММ.ГГГГ")
    birth_date = datetime.date(
        int(date_parse.group(3)), int(date_parse.group(2)), int(date_parse.group(1))
    )

    if birth_date > datetime.datetime.utcnow().date():
        raise ValueError("Дата рождения должна быть меньше текущей даты.")

    return birth_date_str


def validate_address(address: str, name: str) -> str:
    if isinstance(address, str) and 0 < len(address) <= 256 and ADDRESS_FORMAT.search(address):
        return address
    raise ValueError(f"{name} - непустая строка, содержащая хотя бы 1 букву или цифру, не более 256 символов")
