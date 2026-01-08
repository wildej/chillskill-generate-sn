"""
Unit тесты для модуля serial_number.py
"""
from datetime import datetime, timezone, timedelta
from serial_number import (
    get_quarter_and_milliseconds,
    get_current_quarter_info,
    luhn_checksum,
    generate_serial_number,
    parse_serial_number,
    validate_serial_number,
    Q1_2026_START
)


class TestGetQuarterAndMilliseconds:
    """Тесты для функции get_quarter_and_milliseconds"""
    
    def test_q1_2026_start(self):
        """Тест начала Q1 2026"""
        quarter, ms = get_quarter_and_milliseconds(0)
        assert quarter == 1
        assert ms == 0
    
    def test_q1_2026_middle(self):
        """Тест середины Q1 2026"""
        # 1 февраля 2026, 12:00:00 UTC
        days = 31  # январь
        hours = 12
        ms = (days * 24 * 60 * 60 + hours * 60 * 60) * 1000
        quarter, ms_in_quarter = get_quarter_and_milliseconds(ms)
        assert quarter == 1
        assert ms_in_quarter == ms
    
    def test_q2_2026_start(self):
        """Тест начала Q2 2026"""
        # 1 апреля 2026, 00:00:00 UTC
        days_in_q1 = 90  # январь (31) + февраль (28) + март (31) = 90 дней
        ms = days_in_q1 * 24 * 60 * 60 * 1000
        quarter, ms_in_quarter = get_quarter_and_milliseconds(ms)
        assert quarter == 2
        assert ms_in_quarter == 0
    
    def test_q3_2026_start(self):
        """Тест начала Q3 2026"""
        # 1 июля 2026, 00:00:00 UTC
        days_in_q1_q2 = 181  # Q1 (90) + Q2 (91) = 181 день
        ms = days_in_q1_q2 * 24 * 60 * 60 * 1000
        quarter, ms_in_quarter = get_quarter_and_milliseconds(ms)
        assert quarter == 3
        assert ms_in_quarter == 0
    
    def test_q4_2026_start(self):
        """Тест начала Q4 2026"""
        # 1 октября 2026, 00:00:00 UTC
        days_in_q1_q2_q3 = 273  # Q1 (90) + Q2 (91) + Q3 (92) = 273 дня
        ms = days_in_q1_q2_q3 * 24 * 60 * 60 * 1000
        quarter, ms_in_quarter = get_quarter_and_milliseconds(ms)
        assert quarter == 4
        assert ms_in_quarter == 0
    
    def test_q1_2027_start(self):
        """Тест начала Q1 2027"""
        # 1 января 2027, 00:00:00 UTC
        days_in_2026 = 365  # 2026 год (не високосный)
        ms = days_in_2026 * 24 * 60 * 60 * 1000
        quarter, ms_in_quarter = get_quarter_and_milliseconds(ms)
        assert quarter == 5  # 5-й квартал (Q1 2027)
        assert ms_in_quarter == 0


class TestGetCurrentQuarterInfo:
    """Тесты для функции get_current_quarter_info"""
    
    def test_returns_tuple(self):
        """Тест что функция возвращает кортеж"""
        quarter, ms = get_current_quarter_info()
        assert isinstance(quarter, int)
        assert isinstance(ms, int)
        assert quarter >= 1
        assert ms >= 0


class TestLuhnChecksum:
    """Тесты для функции luhn_checksum"""
    
    def test_simple_case(self):
        """Простой тест алгоритма Луна"""
        # Пример: "7992739871" должна иметь контрольную сумму 3
        checksum = luhn_checksum("7992739871")
        assert checksum == 3
    
    def test_zero_checksum(self):
        """Тест когда контрольная сумма равна 0"""
        # "00000000000" должна иметь контрольную сумму 0
        checksum = luhn_checksum("00000000000")
        assert checksum == 0
    
    def test_single_digit(self):
        """Тест с одной цифрой"""
        checksum = luhn_checksum("5")
        assert 0 <= checksum <= 9
    
    def test_quarter_and_ms_format(self):
        """Тест формата используемого в серийных номерах"""
        # Тест для формата "01" + "00000000000"
        checksum = luhn_checksum("0100000000000")
        assert 0 <= checksum <= 9
    
    def test_known_luhn_examples(self):
        """Тест известных примеров алгоритма Луна"""
        # Пример из википедии: "7992739871" -> checksum = 3
        assert luhn_checksum("7992739871") == 3
        # Проверка что "79927398713" валидна (последняя цифра - checksum)
        # Это означает что luhn("7992739871") должна быть 3


class TestGenerateSerialNumber:
    """Тесты для функции generate_serial_number"""
    
    def test_format_structure(self):
        """Тест структуры формата серийного номера"""
        serial = generate_serial_number(0, 0)
        # Формат: XX-YYYY-YYYY-YYYZ
        parts = serial.split("-")
        assert len(parts) == 4
        assert len(parts[0]) == 2  # XX
        assert len(parts[1]) == 4  # YYYY
        assert len(parts[2]) == 4  # YYYY
        assert len(parts[3]) == 4  # YYYZ
    
    def test_q1_2026_start(self):
        """Тест генерации для начала Q1 2026"""
        serial = generate_serial_number(0, 0)
        assert serial.startswith("01-")  # Q1 2026
        assert serial.endswith("-0000")  # 0 миллисекунд
    
    def test_uniqueness_with_offset(self):
        """Тест уникальности при использовании offset"""
        serial1 = generate_serial_number(1000, 0)
        serial2 = generate_serial_number(1000, 1)
        assert serial1 != serial2
    
    def test_quarter_increment(self):
        """Тест что номер квартала увеличивается правильно"""
        # Q1 2026 начало
        serial_q1 = generate_serial_number(0, 0)
        quarter_q1 = int(serial_q1.split("-")[0])
        assert quarter_q1 == 1
        
        # Q2 2026 начало (примерно 90 дней)
        days_q2 = 90 * 24 * 60 * 60 * 1000
        serial_q2 = generate_serial_number(days_q2, 0)
        quarter_q2 = int(serial_q2.split("-")[0])
        assert quarter_q2 == 2
    
    def test_generated_serial_is_valid(self):
        """Тест что сгенерированный серийный номер валиден"""
        serial = generate_serial_number(1000000, 0)
        is_valid, error, _ = validate_serial_number(serial)
        assert is_valid, f"Generated serial {serial} is not valid: {error}"


class TestParseSerialNumber:
    """Тесты для функции parse_serial_number"""
    
    def test_valid_format(self):
        """Тест парсинга валидного формата"""
        serial = "01-0000-0000-0000"
        result = parse_serial_number(serial)
        assert result is not None
        quarter, ms, checksum = result
        assert quarter == 1
        assert ms == 0
        assert checksum == 0
    
    def test_invalid_format_wrong_parts(self):
        """Тест неверного формата - неправильное количество частей"""
        assert parse_serial_number("01-0000-0000") is None
        assert parse_serial_number("01-0000-0000-0000-0000") is None
    
    def test_invalid_format_wrong_lengths(self):
        """Тест неверного формата - неправильные длины частей"""
        assert parse_serial_number("1-0000-0000-0000") is None  # XX должен быть 2 цифры
        assert parse_serial_number("01-000-0000-0000") is None  # YYYY должен быть 4 цифры
        assert parse_serial_number("01-0000-000-0000") is None  # YYYY должен быть 4 цифры
        assert parse_serial_number("01-0000-0000-000") is None  # YYYZ должен быть 4 цифры
    
    def test_with_spaces(self):
        """Тест что пробелы игнорируются"""
        serial = "01 - 0000 - 0000 - 0000"
        result = parse_serial_number(serial)
        assert result is not None
        quarter, ms, checksum = result
        assert quarter == 1
        assert ms == 0
        assert checksum == 0
    
    def test_parse_generated_serial(self):
        """Тест парсинга сгенерированного серийного номера"""
        serial = generate_serial_number(123456789, 0)
        result = parse_serial_number(serial)
        assert result is not None
        quarter, ms, checksum = result
        assert isinstance(quarter, int)
        assert isinstance(ms, int)
        assert isinstance(checksum, int)
        assert 0 <= checksum <= 9


class TestValidateSerialNumber:
    """Тесты для функции validate_serial_number"""
    
    def test_valid_generated_serial(self):
        """Тест валидации сгенерированного серийного номера"""
        serial = generate_serial_number(1000000, 0)
        is_valid, error, date = validate_serial_number(serial)
        assert is_valid, f"Valid serial failed: {error}"
        assert error is None
        assert date is not None
        assert "." in date  # Формат MM.YYYY
    
    def test_invalid_format(self):
        """Тест валидации неверного формата"""
        is_valid, error, date = validate_serial_number("invalid")
        assert not is_valid
        assert error == "Неверный формат серийного номера"
        assert date is None
    
    def test_invalid_checksum(self):
        """Тест валидации с неверной контрольной суммой"""
        # Генерируем валидный номер
        serial = generate_serial_number(1000000, 0)
        # Меняем последнюю цифру (контрольную сумму)
        parts = serial.split("-")
        last_part = parts[3]
        wrong_checksum = (int(last_part[-1]) + 1) % 10
        wrong_serial = f"{parts[0]}-{parts[1]}-{parts[2]}-{last_part[:-1]}{wrong_checksum}"
        
        is_valid, error, date = validate_serial_number(wrong_serial)
        assert not is_valid
        assert error == "Неверная контрольная сумма"
        assert date is None
    
    def test_structure_validation(self):
        """Тест валидации структуры серийного номера"""
        # Неверная структура - недостаточно частей
        is_valid, error, date = validate_serial_number("01-0000-0000")
        assert not is_valid
        assert error == "Неверный формат серийного номера"
        
        # Неверная структура - неправильные длины
        is_valid, error, date = validate_serial_number("1-0000-0000-0000")
        assert not is_valid
        assert error == "Неверный формат серийного номера"
    
    def test_checksum_validation(self):
        """Тест валидации контрольной суммы"""
        # Генерируем несколько валидных номеров и проверяем
        for offset in range(10):
            serial = generate_serial_number(1000000, offset)
            is_valid, error, date = validate_serial_number(serial)
            assert is_valid, f"Serial {serial} should be valid: {error}"
            assert error is None
    
    def test_generation_date(self):
        """Тест что дата генерации вычисляется правильно"""
        # Q1 2026 (квартал 1) -> январь 2026 -> 01.2026
        serial = generate_serial_number(0, 0)
        is_valid, error, date = validate_serial_number(serial)
        assert is_valid
        assert date == "01.2026"
        
        # Q2 2026 (квартал 2) -> апрель 2026 -> 04.2026
        days_q2 = 90 * 24 * 60 * 60 * 1000
        serial_q2 = generate_serial_number(days_q2, 0)
        is_valid, error, date = validate_serial_number(serial_q2)
        assert is_valid
        assert date == "04.2026"
        
        # Q3 2026 (квартал 3) -> июль 2026 -> 07.2026
        days_q3 = 181 * 24 * 60 * 60 * 1000
        serial_q3 = generate_serial_number(days_q3, 0)
        is_valid, error, date = validate_serial_number(serial_q3)
        assert is_valid
        assert date == "07.2026"
        
        # Q4 2026 (квартал 4) -> октябрь 2026 -> 10.2026
        days_q4 = 273 * 24 * 60 * 60 * 1000
        serial_q4 = generate_serial_number(days_q4, 0)
        is_valid, error, date = validate_serial_number(serial_q4)
        assert is_valid
        assert date == "10.2026"
    
    def test_multiple_generated_serials_are_valid(self):
        """Модульный тест: проверка что все сгенерированные номера валидны"""
        # Генерируем множество серийных номеров и проверяем их валидность
        base_timestamp = 1000000
        for offset in range(100):
            serial = generate_serial_number(base_timestamp, offset)
            is_valid, error, date = validate_serial_number(serial)
            assert is_valid, f"Generated serial {serial} is not valid: {error}"
            assert date is not None
    
    def test_round_trip_validation(self):
        """Тест полного цикла: генерация -> валидация -> парсинг"""
        for offset in range(20):
            serial = generate_serial_number(1000000, offset)
            # Валидация
            is_valid, error, date = validate_serial_number(serial)
            assert is_valid, f"Serial {serial} failed validation: {error}"
            # Парсинг
            parsed = parse_serial_number(serial)
            assert parsed is not None, f"Serial {serial} failed parsing"
            quarter, ms, checksum = parsed
            # Проверка что контрольная сумма правильная
            quarter_str = f"{quarter:02d}"
            ms_str = f"{ms:011d}"
            calculated_checksum = luhn_checksum(quarter_str + ms_str)
            assert checksum == calculated_checksum, \
                f"Checksum mismatch for serial {serial}: expected {calculated_checksum}, got {checksum}"
