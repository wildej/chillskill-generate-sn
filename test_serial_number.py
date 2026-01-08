"""
Модульные тесты для функции get_quarter_number_since_q1_2026.
"""
import pytest
from datetime import datetime, timezone
from serial_number import get_quarter_number_since_q1_2026, get_quarter_number, get_seconds_since_quarter_start, Q1_2026_START, generate_serial_number, parse_serial_number
from luhn_algorithm import calculate_luhn_checksum, add_valid_luhn_checksum, validate_luhn_checksum


class TestGetQuarter:
    """Тесты для функции get_quarter_number_since_q1_2026."""
    
    def test_q1_2026_start(self):
        """Тест начала Q1 2026."""
        time = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 1
    
    def test_q1_2026_middle(self):
        """Тест середины Q1 2026."""
        time = datetime(2026, 2, 15, 12, 30, 0, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 1
    
    def test_q1_2026_end(self):
        """Тест конца Q1 2026."""
        time = datetime(2026, 3, 31, 23, 59, 59, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 1
    
    def test_q2_2026_start(self):
        """Тест начала Q2 2026."""
        time = datetime(2026, 4, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 2
    
    def test_q2_2026_middle(self):
        """Тест середины Q2 2026."""
        time = datetime(2026, 5, 15, 12, 30, 0, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 2
    
    def test_q2_2026_end(self):
        """Тест конца Q2 2026."""
        time = datetime(2026, 6, 30, 23, 59, 59, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 2
    
    def test_q3_2026_start(self):
        """Тест начала Q3 2026."""
        time = datetime(2026, 7, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 3
    
    def test_q3_2026_middle(self):
        """Тест середины Q3 2026."""
        time = datetime(2026, 8, 15, 12, 30, 0, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 3
    
    def test_q3_2026_end(self):
        """Тест конца Q3 2026."""
        time = datetime(2026, 9, 30, 23, 59, 59, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 3
    
    def test_q4_2026_start(self):
        """Тест начала Q4 2026."""
        time = datetime(2026, 10, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 4
    
    def test_q4_2026_middle(self):
        """Тест середины Q4 2026."""
        time = datetime(2026, 11, 15, 12, 30, 0, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 4
    
    def test_q4_2026_end(self):
        """Тест конца Q4 2026."""
        time = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 4
    
    def test_q1_2027(self):
        """Тест Q1 2027."""
        time = datetime(2027, 2, 15, 12, 30, 0, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 5
    
    def test_q2_2027(self):
        """Тест Q2 2027."""
        time = datetime(2027, 5, 15, 12, 30, 0, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 6
    
    def test_q3_2027(self):
        """Тест Q3 2027."""
        time = datetime(2027, 8, 15, 12, 30, 0, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 7
    
    def test_q4_2027(self):
        """Тест Q4 2027."""
        time = datetime(2027, 11, 15, 12, 30, 0, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 8
    
    def test_q1_2028(self):
        """Тест Q1 2028."""
        time = datetime(2028, 2, 15, 12, 30, 0, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 9
    
    def test_different_timezones(self):
        """Тест с разными часовыми поясами."""
        # UTC
        time_utc = datetime(2026, 6, 15, 12, 0, 0, tzinfo=timezone.utc)
        quarter_utc = get_quarter_number_since_q1_2026(time_utc)
        
        # UTC+3 (Москва)
        time_msk = datetime(2026, 6, 15, 15, 0, 0, tzinfo=timezone.utc)
        quarter_msk = get_quarter_number_since_q1_2026(time_msk)
        
        # Оба должны быть в одном квартале (Q2 2026)
        assert quarter_utc == 2
        assert quarter_msk == 2
    
    def test_edge_case_last_second_of_year(self):
        """Тест последней секунды года."""
        time = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 4
    
    def test_edge_case_first_second_of_next_year(self):
        """Тест первой секунды следующего года."""
        time = datetime(2027, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number_since_q1_2026(time) == 5


class TestGetQuarterNumber:
    """Тесты для функции get_quarter_number."""
    
    def test_q1_january(self):
        """Тест января (Q1)."""
        time = datetime(2026, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 1
    
    def test_q1_february(self):
        """Тест февраля (Q1)."""
        time = datetime(2026, 2, 15, 12, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 1
    
    def test_q1_march(self):
        """Тест марта (Q1)."""
        time = datetime(2026, 3, 15, 12, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 1
    
    def test_q2_april(self):
        """Тест апреля (Q2)."""
        time = datetime(2026, 4, 15, 12, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 2
    
    def test_q2_may(self):
        """Тест мая (Q2)."""
        time = datetime(2026, 5, 15, 12, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 2
    
    def test_q2_june(self):
        """Тест июня (Q2)."""
        time = datetime(2026, 6, 15, 12, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 2
    
    def test_q3_july(self):
        """Тест июля (Q3)."""
        time = datetime(2026, 7, 15, 12, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 3
    
    def test_q3_august(self):
        """Тест августа (Q3)."""
        time = datetime(2026, 8, 15, 12, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 3
    
    def test_q3_september(self):
        """Тест сентября (Q3)."""
        time = datetime(2026, 9, 15, 12, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 3
    
    def test_q4_october(self):
        """Тест октября (Q4)."""
        time = datetime(2026, 10, 15, 12, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 4
    
    def test_q4_november(self):
        """Тест ноября (Q4)."""
        time = datetime(2026, 11, 15, 12, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 4
    
    def test_q4_december(self):
        """Тест декабря (Q4)."""
        time = datetime(2026, 12, 15, 12, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 4
    
    def test_q1_start_of_year(self):
        """Тест начала года (1 января)."""
        time = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 1
    
    def test_q1_end_of_march(self):
        """Тест конца марта (последний день Q1)."""
        time = datetime(2026, 3, 31, 23, 59, 59, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 1
    
    def test_q2_start_of_april(self):
        """Тест начала апреля (первый день Q2)."""
        time = datetime(2026, 4, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time) == 2
    
    def test_different_years_same_quarter(self):
        """Тест того, что функция возвращает номер квартала в году, а не абсолютный."""
        time_2026 = datetime(2026, 2, 15, 12, 0, 0, tzinfo=timezone.utc)
        time_2027 = datetime(2027, 2, 15, 12, 0, 0, tzinfo=timezone.utc)
        assert get_quarter_number(time_2026) == 1
        assert get_quarter_number(time_2027) == 1


class TestGetSecondsSinceQuarterStart:
    """Тесты для функции get_seconds_since_quarter_start."""
    
    def test_start_of_quarter(self):
        """Тест начала квартала (0 секунд)."""
        time = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert get_seconds_since_quarter_start(time) == 0
    
    def test_one_second_after_start(self):
        """Тест одной секунды после начала квартала."""
        time = datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc)
        assert get_seconds_since_quarter_start(time) == 1
    
    def test_one_minute_after_start(self):
        """Тест одной минуты после начала квартала."""
        time = datetime(2026, 1, 1, 0, 1, 0, tzinfo=timezone.utc)
        assert get_seconds_since_quarter_start(time) == 60
    
    def test_one_hour_after_start(self):
        """Тест одного часа после начала квартала."""
        time = datetime(2026, 1, 1, 1, 0, 0, tzinfo=timezone.utc)
        assert get_seconds_since_quarter_start(time) == 3600
    
    def test_one_day_after_start(self):
        """Тест одного дня после начала квартала."""
        time = datetime(2026, 1, 2, 0, 0, 0, tzinfo=timezone.utc)
        assert get_seconds_since_quarter_start(time) == 86400
    
    def test_middle_of_january(self):
        """Тест середины января."""
        time = datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        expected_seconds = (
            (15 - 1) * 86400 +  # дни
            12 * 3600 +         # часы
            30 * 60 +           # минуты
            45                  # секунды
        )
        assert get_seconds_since_quarter_start(time) == expected_seconds
    
    def test_start_of_q2(self):
        """Тест начала Q2 (0 секунд)."""
        time = datetime(2026, 4, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert get_seconds_since_quarter_start(time) == 0
    
    def test_middle_of_april(self):
        """Тест середины апреля."""
        time = datetime(2026, 4, 15, 12, 30, 45, tzinfo=timezone.utc)
        expected_seconds = (
            (15 - 1) * 86400 +  # дни
            12 * 3600 +         # часы
            30 * 60 +           # минуты
            45                  # секунды
        )
        assert get_seconds_since_quarter_start(time) == expected_seconds
    
    def test_start_of_q3(self):
        """Тест начала Q3 (0 секунд)."""
        time = datetime(2026, 7, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert get_seconds_since_quarter_start(time) == 0
    
    def test_start_of_q4(self):
        """Тест начала Q4 (0 секунд)."""
        time = datetime(2026, 10, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert get_seconds_since_quarter_start(time) == 0
    
    def test_end_of_march(self):
        """Тест конца марта (последний день Q1)."""
        time = datetime(2026, 3, 31, 23, 59, 59, tzinfo=timezone.utc)
        # 31 января + 28 февраля (2026 не високосный) + 30 марта = 89 дней
        # 89 дней * 86400 + 23*3600 + 59*60 + 59
        expected_seconds = (
            89 * 86400 +        # дни (31 + 28 + 30)
            23 * 3600 +         # часы
            59 * 60 +           # минуты
            59                  # секунды
        )
        assert get_seconds_since_quarter_start(time) == expected_seconds
    
    def test_end_of_june(self):
        """Тест конца июня (последний день Q2)."""
        time = datetime(2026, 6, 30, 23, 59, 59, tzinfo=timezone.utc)
        # 30 апреля + 31 мая + 29 июня = 90 дней
        expected_seconds = (
            90 * 86400 +        # дни (30 + 31 + 29)
            23 * 3600 +         # часы
            59 * 60 +           # минуты
            59                  # секунды
        )
        assert get_seconds_since_quarter_start(time) == expected_seconds
    
    def test_february_29_leap_year(self):
        """Тест 29 февраля в високосном году."""
        time = datetime(2028, 2, 29, 12, 0, 0, tzinfo=timezone.utc)
        # От начала квартала (1 января) до 29 февраля 12:00:00 = 59.5 дня
        # Проверяем, что функция корректно обрабатывает високосный год
        result = get_seconds_since_quarter_start(time)
        assert result == 5140800.0  # 59.5 дня = 59 * 86400 + 12 * 3600
        assert result / 86400 == 59.5  # Проверка в днях
    
    def test_different_years_same_quarter(self):
        """Тест того, что функция считает секунды от начала квартала в конкретном году."""
        time_2026_q1 = datetime(2026, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        time_2027_q1 = datetime(2027, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        # Оба должны иметь одинаковое количество секунд от начала своего квартала
        seconds_2026 = get_seconds_since_quarter_start(time_2026_q1)
        seconds_2027 = get_seconds_since_quarter_start(time_2027_q1)
        assert seconds_2026 == seconds_2027
        assert seconds_2026 == (14 * 86400 + 12 * 3600)


class TestCalculateLuhnChecksum:
    """Тесты для функции calculate_luhn_checksum."""
    
    def test_example_456126121234546(self):
        """Тест для примера 456126121234546 -> 8."""
        number = "456126121234546"
        assert calculate_luhn_checksum(number) == 8
    
    def test_example_7992739871(self):
        """Тест для примера 7992739871 -> 6."""
        number = "7992739871"
        assert calculate_luhn_checksum(number) == 6


class TestAddValidLuhnChecksum:
    """Тесты для функции add_valid_luhn_checksum."""
    
    def test_basic_functionality(self):
        """Тест базовой функциональности - результат должен иметь валидную контрольную сумму."""
        number = "123456789"
        result = add_valid_luhn_checksum(number)
        # Результат должен быть длиннее исходного числа на 1 символ
        assert len(result) == len(number) + 1
        # Результат должен начинаться с исходного числа
        assert result.startswith(number)
        # Контрольная сумма должна быть валидной
        assert validate_luhn_checksum(result)
    
    def test_single_digit(self):
        """Тест для однозначного числа."""
        number = "5"
        result = add_valid_luhn_checksum(number)
        assert len(result) == 2
        assert result.startswith(number)
        assert validate_luhn_checksum(result)
    
    def test_two_digits(self):
        """Тест для двузначного числа."""
        number = "42"
        result = add_valid_luhn_checksum(number)
        assert len(result) == 3
        assert result.startswith(number)
        assert validate_luhn_checksum(result)
    
    def test_empty_string(self):
        """Тест для пустой строки."""
        number = ""
        result = add_valid_luhn_checksum(number)
        # Результат должен содержать ровно одну цифру и быть валидным
        assert len(result) == 1, f"Результат должен содержать ровно одну цифру, получено: '{result}'"
        assert validate_luhn_checksum(result), f"Результат '{result}' должен иметь валидную контрольную сумму"
    
    def test_long_number(self):
        """Тест для длинного числа."""
        number = "12345678901234567890"
        result = add_valid_luhn_checksum(number)
        assert len(result) == len(number) + 1
        assert result.startswith(number)
        assert validate_luhn_checksum(result)
    
    def test_example_456126121234546(self):
        """Тест для примера 456126121234546."""
        number = "456126121234546"
        result = add_valid_luhn_checksum(number)
        # Проверяем, что результат валиден
        assert validate_luhn_checksum(result)
        # Проверяем, что добавлена одна цифра
        assert len(result) == len(number) + 1
        assert result.startswith(number)
    
    def test_example_7992739871(self):
        """Тест для примера 7992739871."""
        number = "7992739871"
        result = add_valid_luhn_checksum(number)
        # Проверяем, что результат валиден
        assert validate_luhn_checksum(result)
        # Проверяем, что добавлена одна цифра
        assert len(result) == len(number) + 1
        assert result.startswith(number)
    
    def test_all_digits_zero(self):
        """Тест для числа из нулей."""
        number = "0000"
        result = add_valid_luhn_checksum(number)
        # Результат должен начинаться с исходного числа
        assert result.startswith(number)
        # Должна быть добавлена ровно одна цифра
        assert len(result) == len(number) + 1, f"Должна быть добавлена ровно одна цифра, получено: '{result}'"
        # Результат должен быть валидным
        assert validate_luhn_checksum(result), f"Результат '{result}' должен иметь валидную контрольную сумму"
    
    def test_all_digits_nine(self):
        """Тест для числа из девяток."""
        number = "9999"
        result = add_valid_luhn_checksum(number)
        assert len(result) == 5
        assert result.startswith(number)
        assert validate_luhn_checksum(result)
    
    def test_alternating_digits(self):
        """Тест для чередующихся цифр."""
        number = "1234567890"
        result = add_valid_luhn_checksum(number)
        assert len(result) == 11
        assert result.startswith(number)
        assert validate_luhn_checksum(result)
    
    def test_checksum_zero_case(self):
        """Тест случая, когда контрольная сумма уже равна 0."""
        # Если checksum = 0, то добавляется 0 (10 - 0 = 10, но берется последняя цифра)
        # На самом деле, если checksum = 0, то 10 - 0 = 10, но мы берем str(10), что даст "10"
        # Нужно проверить, что функция корректно обрабатывает этот случай
        # Попробуем найти число, для которого checksum будет 0
        number = "123456789012345"
        result = add_valid_luhn_checksum(number)
        assert validate_luhn_checksum(result)
    
    def test_multiple_calls_consistency(self):
        """Тест консистентности - повторный вызов на том же числе должен дать тот же результат."""
        number = "123456789"
        result1 = add_valid_luhn_checksum(number)
        result2 = add_valid_luhn_checksum(number)
        assert result1 == result2
        assert validate_luhn_checksum(result1)
        assert validate_luhn_checksum(result2)
    
    def test_known_valid_number(self):
        """Тест с известным валидным числом - проверяем, что функция не меняет его."""
        # Если число уже валидно, функция все равно добавит цифру
        # Это нормально, так как функция всегда добавляет цифру
        number = "79927398713"  # Это валидное число по алгоритму Луна
        result = add_valid_luhn_checksum(number)
        # Функция все равно добавит еще одну цифру
        assert len(result) == len(number) + 1
        assert validate_luhn_checksum(result)


class TestGenerateSerialNumber:
    """Дымовой тест для функции generate_serial_number."""
    
    def test_generate_and_validate(self):
        """Тест генерации серийного номера и его валидации."""
        time = datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        
        # Проверяем, что серийный номер был сгенерирован
        assert serial_number is not None
        assert isinstance(serial_number, str)
        assert len(serial_number) > 0
        
        # Проверяем, что сгенерированный серийный номер проходит валидацию
        assert validate_luhn_checksum(serial_number)


class TestValidateSerialNumber:
    """Тесты для функции parse_serial_number."""
    
    def test_valid_serial_number_q1_2026(self):
        """Тест валидного серийного номера для Q1 2026."""
        time = datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        
        is_valid, message = parse_serial_number(serial_number)
        assert is_valid is True
        assert "I квартал 26 года" in message
    
    def test_valid_serial_number_q2_2026(self):
        """Тест валидного серийного номера для Q2 2026."""
        time = datetime(2026, 5, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        
        is_valid, message = parse_serial_number(serial_number)
        assert is_valid is True
        assert "II квартал 26 года" in message
    
    def test_valid_serial_number_q3_2026(self):
        """Тест валидного серийного номера для Q3 2026."""
        time = datetime(2026, 8, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        
        is_valid, message = parse_serial_number(serial_number)
        assert is_valid is True
        assert "III квартал 26 года" in message
    
    def test_valid_serial_number_q4_2026(self):
        """Тест валидного серийного номера для Q4 2026."""
        time = datetime(2026, 11, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        
        is_valid, message = parse_serial_number(serial_number)
        assert is_valid is True
        assert "IV квартал 26 года" in message
    
    def test_valid_serial_number_q1_2027(self):
        """Тест валидного серийного номера для Q1 2027."""
        time = datetime(2027, 2, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        
        is_valid, message = parse_serial_number(serial_number)
        assert is_valid is True
        assert "I квартал 27 года" in message
    
    def test_valid_serial_number_with_dashes(self):
        """Тест валидного серийного номера с дефисами."""
        time = datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        formatted = f"{serial_number[0:4]}-{serial_number[4:8]}-{serial_number[8:12]}"
        
        is_valid, message = parse_serial_number(formatted)
        assert is_valid is True
        assert "I квартал 26 года" in message
    
    def test_valid_serial_number_with_spaces(self):
        """Тест валидного серийного номера с пробелами."""
        time = datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        formatted = f"{serial_number[0:4]} {serial_number[4:8]} {serial_number[8:12]}"
        
        is_valid, message = parse_serial_number(formatted)
        assert is_valid is True
        assert "I квартал 26 года" in message
    
    def test_valid_serial_number_mixed_formatting(self):
        """Тест валидного серийного номера со смешанным форматированием."""
        time = datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        formatted = f"{serial_number[0:4]}-{serial_number[4:8]} {serial_number[8:12]}"
        
        is_valid, message = parse_serial_number(formatted)
        assert is_valid is True
        assert "I квартал 26 года" in message
    
    def test_invalid_serial_number_too_short(self):
        """Тест невалидного серийного номера (слишком короткий)."""
        serial_number = "12345678901"  # 11 цифр вместо 12
        
        is_valid, message = parse_serial_number(serial_number)
        assert is_valid is False
        assert "12 цифр" in message
    
    def test_invalid_serial_number_too_long(self):
        """Тест невалидного серийного номера (слишком длинный)."""
        serial_number = "1234567890123"  # 13 цифр вместо 12
        
        is_valid, message = parse_serial_number(serial_number)
        assert is_valid is False
        assert "12 цифр" in message
    
    def test_invalid_serial_number_empty(self):
        """Тест пустого серийного номера."""
        serial_number = ""
        
        is_valid, message = parse_serial_number(serial_number)
        assert is_valid is False
        assert "12 цифр" in message
    
    def test_invalid_serial_number_only_spaces(self):
        """Тест серийного номера только из пробелов."""
        serial_number = "   -  -  "
        
        is_valid, message = parse_serial_number(serial_number)
        assert is_valid is False
        assert "12 цифр" in message
    
    def test_invalid_serial_number_wrong_checksum(self):
        """Тест невалидного серийного номера с неправильной контрольной суммой."""
        # Создаем валидный номер и меняем последнюю цифру
        time = datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        # Меняем последнюю цифру
        invalid_serial = serial_number[:-1] + str((int(serial_number[-1]) + 1) % 10)
        
        is_valid, message = parse_serial_number(invalid_serial)
        assert is_valid is False
        assert "опечатка" in message or "корректность" in message
    
    def test_invalid_serial_number_wrong_checksum_middle(self):
        """Тест невалидного серийного номера с измененной цифрой в середине."""
        # Создаем валидный номер и меняем цифру в середине
        time = datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        # Меняем цифру в середине
        invalid_serial = serial_number[:6] + str((int(serial_number[6]) + 1) % 10) + serial_number[7:]
        
        is_valid, message = parse_serial_number(invalid_serial)
        assert is_valid is False
        assert "опечатка" in message or "корректность" in message
    
    def test_valid_serial_number_all_zeros(self):
        """Тест серийного номера из нулей (если он валиден по Луну)."""
        # Проверяем, что "000000000000" не валиден по Луну
        serial_number = "000000000000"
        
        is_valid, message = parse_serial_number(serial_number)
        # Если контрольная сумма неверна, должна быть ошибка
        # Если валидна, то должна быть успешная валидация
        # Проверим фактический результат
        if validate_luhn_checksum(serial_number):
            assert is_valid is True
        else:
            assert is_valid is False
    
    def test_valid_serial_number_different_adds(self):
        """Тест валидных серийных номеров с разными добавочными числами."""
        time = datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        
        for adds in [0, 1, 42, 99]:
            serial_number = generate_serial_number(time, adds)
            is_valid, message = parse_serial_number(serial_number)
            assert is_valid is True
            assert "I квартал 26 года" in message
    
    def test_valid_serial_number_different_times_same_quarter(self):
        """Тест валидных серийных номеров для разных времен в одном квартале."""
        adds = 42
        
        # Разные даты в Q1 2026 (теперь все должны давать 12-значные номера благодаря формату :07d)
        times = [
            datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),  # Начало квартала (0 секунд)
            datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc),  # Первая секунда квартала
            datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc),  # Середина января
            datetime(2026, 2, 15, 12, 30, 45, tzinfo=timezone.utc),  # Середина февраля
            datetime(2026, 3, 31, 23, 59, 59, tzinfo=timezone.utc),  # Конец марта
        ]
        
        for time in times:
            serial_number = generate_serial_number(time, adds)
            # Проверяем, что номер всегда 12-значный
            assert len(serial_number) == 12, f"Серийный номер должен быть 12-значным, получено: {len(serial_number)} цифр для времени {time}"
            is_valid, message = parse_serial_number(serial_number)
            assert is_valid is True
            assert "I квартал 26 года" in message
    
    def test_valid_serial_number_early_date(self):
        """Тест валидного серийного номера для ранней даты (начало квартала).
        
        Проверяет, что даже при малом количестве секунд с начала квартала
        генерируется 12-значный номер благодаря формату :07d для секунд.
        """
        adds = 42
        
        # Проверяем самые ранние времена в квартале
        early_times = [
            datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),  # Начало квартала (0 секунд)
            datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc),  # 1 секунда
            datetime(2026, 1, 1, 0, 1, 0, tzinfo=timezone.utc),  # 1 минута
            datetime(2026, 1, 1, 1, 0, 0, tzinfo=timezone.utc),  # 1 час
        ]
        
        for time in early_times:
            serial_number = generate_serial_number(time, adds)
            # Критически важно: номер должен быть ровно 12-значным
            assert len(serial_number) == 12, (
                f"Серийный номер должен быть 12-значным, "
                f"получено: {len(serial_number)} цифр для времени {time}, "
                f"номер: {serial_number}"
            )
            is_valid, message = parse_serial_number(serial_number)
            assert is_valid is True, (
                f"Серийный номер должен быть валидным для времени {time}, "
                f"номер: {serial_number}, сообщение: {message}"
            )
            assert "I квартал 26 года" in message
    
    def test_valid_serial_number_with_letters(self):
        """Тест серийного номера с буквами (должны быть удалены)."""
        time = datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        # Добавляем буквы
        formatted = f"ABC{serial_number}XYZ"
        
        is_valid, message = parse_serial_number(formatted)
        assert is_valid is True
        assert "I квартал 26 года" in message
    
    def test_valid_serial_number_with_special_chars(self):
        """Тест серийного номера со специальными символами (должны быть удалены)."""
        time = datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        # Добавляем специальные символы
        formatted = f"!@#{serial_number}$%^"
        
        is_valid, message = parse_serial_number(formatted)
        assert is_valid is True
        assert "I квартал 26 года" in message
    
    def test_valid_serial_number_q2_2027(self):
        """Тест валидного серийного номера для Q2 2027."""
        time = datetime(2027, 5, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        
        is_valid, message = parse_serial_number(serial_number)
        assert is_valid is True
        assert "II квартал 27 года" in message
    
    def test_valid_serial_number_q4_2027(self):
        """Тест валидного серийного номера для Q4 2027."""
        time = datetime(2027, 11, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        
        is_valid, message = parse_serial_number(serial_number)
        assert is_valid is True
        assert "IV квартал 27 года" in message
    
    def test_valid_serial_number_q1_2028(self):
        """Тест валидного серийного номера для Q1 2028."""
        time = datetime(2028, 2, 15, 12, 30, 45, tzinfo=timezone.utc)
        adds = 42
        serial_number = generate_serial_number(time, adds)
        
        is_valid, message = parse_serial_number(serial_number)
        assert is_valid is True
        assert "I квартал 28 года" in message
