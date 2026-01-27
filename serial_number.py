"""
Модуль для генерации и проверки серийных номеров.
Формат: XXSS SSSS SAAC
- XX: номер квартала (начиная с Q1 2026)
- SSSSSSS: секунды с начала квартала
- AA: добавочные числа
- Z: контрольная сумма по алгоритму Луна
"""
from datetime import datetime, timezone
from typing import Tuple, Optional

from luhn_algorithm import add_valid_luhn_checksum, validate_luhn_checksum

# Дата начала отсчета - 1 января 2026, 00:00:00 UTC
Q1_2026_START = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

def get_quarter_number(time: datetime) -> int:
    """
    Определяет номер квартала в текущем году.
    """
    return (time.month - 1) // 3 + 1

def get_quarter_number_since_q1_2026(time: datetime) -> int:
    """
    Определяет номер квартала начиная с Q1 2026.
    """
    years_diff = time.year - Q1_2026_START.year
    return years_diff * 4 + get_quarter_number(time)

def get_seconds_since_quarter_start(time: datetime) -> int:
    """
    Возвращает количество секунд с начала квартала.
    """
    quarter_number = get_quarter_number(time)

    quarter_start = datetime(time.year, (quarter_number - 1) * 3 + 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    return int((time - quarter_start).total_seconds())

def generate_serial_number(time: datetime, adds: int) -> str:
    """
    Генерирует серийный номер.
    """
    quarter_number = get_quarter_number_since_q1_2026(time)
    seconds = get_seconds_since_quarter_start(time)
    return add_valid_luhn_checksum(f"{quarter_number:02d}{seconds:07d}{adds:02d}")

def format_serial_number(serial: str) -> str:
    """
    Форматирует серийный номер в формат XXXX-XXXX-XXXX.
    """
    return f"{serial[0:4]}-{serial[4:8]}-{serial[8:12]}"

def parse_serial_number(user_input: str) -> Tuple[bool, str, str]:
    """
    Валидирует серийный номер и извлекает информацию о квартале и годе из серийного номера.
    Проверяет что в нем только цифры и что его длина равна 12, а так же что его контрольная сумма валидна.
    """
    # Извлекаем только цифры
    serial = ''.join(filter(str.isdigit, user_input))

    if len(serial) != 12:
        return False, serial, "Серийный номер должен содержать ровно 12 цифр"
    if not validate_luhn_checksum(serial):
        return False, serial, "Проверьте корректность введенного серийного номера, возможна опечатка"
    
    # Извлекаем информацию о квартале и годе из серийного номера
    # serial: строка из 12 цифр (без пробелов и дефисов)
    quarter_roman = {1: "I", 2: "II", 3: "III", 4: "IV"}
    try:
        quarter_and_year = int(serial[:2])
        # Квартал с начала 2026, т.е. 01 - Q1'26, 02 - Q2'26, ..., 05 - Q1'27 и т.д.
        absolute_quarter = quarter_and_year
        year_offset = (absolute_quarter - 1) // 4
        quarter_in_year = ((absolute_quarter - 1) % 4) + 1
        year = 26 + year_offset
        quarter_str = quarter_roman[quarter_in_year]
        date_string = f"{quarter_str} квартал {year:02d} года"
        return True, serial, date_string
    except Exception:
        return True, serial, "Не удалось определить дату из серийного номера"
