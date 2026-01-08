"""
Модуль для генерации и проверки серийных номеров.
Формат: XX-YYYY-YYYY-YYYZ
- XX: номер квартала (начиная с Q1 2026)
- YYYYYYYYYYY: уникальное число (миллисекунды с начала квартала)
- Z: контрольная сумма по алгоритму Луна
"""
from datetime import datetime, timezone
from typing import Tuple, Optional


# Дата начала отсчета - 1 января 2026, 00:00:00 UTC
Q1_2026_START = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)


def get_quarter_and_milliseconds(timestamp_ms: int) -> Tuple[int, int]:
    """
    Определяет номер квартала и миллисекунды с начала квартала.
    
    Args:
        timestamp_ms: Временная метка в миллисекундах с начала Q1 2026
    
    Returns:
        Tuple[номер_квартала, миллисекунды_с_начала_квартала]
    """
    # Преобразуем миллисекунды в datetime
    from datetime import timedelta
    start_datetime = Q1_2026_START
    current_datetime = start_datetime + timedelta(milliseconds=timestamp_ms)
    
    # Определяем текущий квартал и начало этого квартала
    year = current_datetime.year
    month = current_datetime.month
    
    # Определяем номер квартала в году (1-4)
    quarter_in_year = (month - 1) // 3 + 1
    
    # Определяем начало текущего квартала
    quarter_start_month = (quarter_in_year - 1) * 3 + 1
    quarter_start = datetime(year, quarter_start_month, 1, tzinfo=timezone.utc)
    
    # Вычисляем номер квартала начиная с Q1 2026
    years_since_2026 = year - 2026
    quarter = years_since_2026 * 4 + quarter_in_year
    
    # Вычисляем миллисекунды с начала квартала
    diff = current_datetime - quarter_start
    ms_in_quarter = int(diff.total_seconds() * 1000)
    
    return quarter, ms_in_quarter


def get_current_quarter_info() -> Tuple[int, int]:
    """
    Получает текущий номер квартала и миллисекунды с начала квартала.
    
    Returns:
        Tuple[номер_квартала, миллисекунды_с_начала_квартала]
    """
    now = datetime.now(timezone.utc)
    start_timestamp = Q1_2026_START.timestamp()
    current_timestamp = now.timestamp()
    
    # Разница в секундах, переводим в миллисекунды
    diff_ms = int((current_timestamp - start_timestamp) * 1000)
    
    return get_quarter_and_milliseconds(diff_ms)


def luhn_checksum(digits: str) -> int:
    """
    Вычисляет контрольную сумму по алгоритму Луна.
    
    Args:
        digits: Строка из цифр (без контрольной суммы)
    
    Returns:
        Контрольная цифра (0-9)
    """
    def luhn_digit(n: int) -> int:
        doubled = n * 2
        return doubled if doubled < 10 else doubled - 9
    
    # Преобразуем в список цифр
    nums = [int(d) for d in digits]
    
    # Применяем алгоритм Луна (начинаем справа, индексируем с 0)
    total = 0
    for i, num in enumerate(reversed(nums)):
        if i % 2 == 0:
            total += num
        else:
            total += luhn_digit(num)
    
    # Контрольная цифра - это число, которое нужно добавить к total, чтобы получить кратное 10
    checksum = (10 - (total % 10)) % 10
    return checksum


def generate_serial_number(base_timestamp_ms: int, offset: int = 0) -> str:
    """
    Генерирует серийный номер.
    
    Args:
        base_timestamp_ms: Базовое время в миллисекундах с начала Q1 2026
        offset: Смещение для уникальности (используется при генерации нескольких номеров)
    
    Returns:
        Серийный номер в формате XX-YYYY-YYYY-YYYZ
    """
    timestamp_ms = base_timestamp_ms + offset
    quarter, ms_in_quarter = get_quarter_and_milliseconds(timestamp_ms)
    
    # Форматируем номер квартала (2 цифры)
    quarter_str = f"{quarter:02d}"
    
    # Форматируем миллисекунды (11 цифр)
    ms_str = f"{ms_in_quarter:011d}"
    
    # Формируем строку без контрольной суммы: XX + YYYYYYYYYYY
    digits_without_checksum = quarter_str + ms_str
    
    # Вычисляем контрольную сумму
    checksum = luhn_checksum(digits_without_checksum)
    
    # Форматируем результат: XX-YYYY-YYYY-YYYZ
    # Разбиваем ms_str на группы: YYYY-YYYY-YYY, последняя часть YYYZ (YYY + checksum)
    formatted_ms = f"{ms_str[:4]}-{ms_str[4:8]}-{ms_str[8:11]}{checksum}"
    
    serial_number = f"{quarter_str}-{formatted_ms}"
    
    return serial_number


def parse_serial_number(serial: str) -> Optional[Tuple[int, int, int]]:
    """
    Парсит серийный номер и извлекает компоненты.
    
    Args:
        serial: Серийный номер в формате XX-YYYY-YYYY-YYYZ
    
    Returns:
        Tuple[quarter, ms_in_quarter, checksum] или None если формат неверный
    """
    try:
        # Удаляем пробелы для проверки, но сохраняем дефисы для парсинга структуры
        serial_clean = serial.replace(" ", "")
        
        # Проверяем формат с дефисами: XX-YYYY-YYYY-YYYZ
        parts = serial_clean.split("-")
        if len(parts) != 4:
            return None
        
        if len(parts[0]) != 2 or len(parts[1]) != 4 or len(parts[2]) != 4 or len(parts[3]) != 4:
            return None
        
        # Извлекаем компоненты
        quarter = int(parts[0])
        ms_part1 = parts[1]  # YYYY (первые 4 цифры миллисекунд)
        ms_part2 = parts[2]  # YYYY (следующие 4 цифры миллисекунд)
        last_part = parts[3]  # YYYZ (последние 3 цифры миллисекунд + 1 цифра checksum)
        
        ms_str = ms_part1 + ms_part2 + last_part[:3]  # YYYYYYYYYYY (11 цифр)
        checksum = int(last_part[3])  # Z (последняя цифра)
        
        ms_in_quarter = int(ms_str)
        
        return quarter, ms_in_quarter, checksum
    except (ValueError, IndexError):
        return None


def validate_serial_number(serial: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Проверяет серийный номер на валидность.
    
    Args:
        serial: Серийный номер для проверки
    
    Returns:
        Tuple[is_valid, error_message, generation_date]
        - is_valid: True если номер валиден
        - error_message: Сообщение об ошибке или None
        - generation_date: Дата генерации в формате MM.YYYY или None
    """
    # Парсим серийный номер
    parsed = parse_serial_number(serial)
    if parsed is None:
        return False, "Неверный формат серийного номера", None
    
    quarter, ms_in_quarter, checksum = parsed
    
    # Проверяем контрольную сумму
    quarter_str = f"{quarter:02d}"
    ms_str = f"{ms_in_quarter:011d}"
    digits_without_checksum = quarter_str + ms_str
    
    calculated_checksum = luhn_checksum(digits_without_checksum)
    
    if checksum != calculated_checksum:
        return False, "Неверная контрольная сумма", None
    
    # Вычисляем дату генерации
    # Квартал начинается с Q1 2026
    year = 2026 + ((quarter - 1) // 4)
    quarter_in_year = ((quarter - 1) % 4) + 1
    month = (quarter_in_year - 1) * 3 + 1  # 1, 4, 7, 10
    
    generation_date = f"{month:02d}.{year}"
    
    return True, None, generation_date
