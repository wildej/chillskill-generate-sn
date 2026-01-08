"""
Модуль для алгоритма Луна проверки контрольной суммы.
"""

def calculate_luhn_checksum(number: str) -> int:
    """
    Рассчитывает контрольную сумму по алгоритму Луна.
    """
    checksum = 0
    for i, digit in enumerate(reversed(number)):
        digit = int(digit)
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        print(digit)
        checksum += digit
    return checksum % 10

def validate_luhn_checksum(number: str) -> bool:
    """
    Проверяет контрольную сумму по алгоритму Луна.
    """
    return calculate_luhn_checksum(number) == 0

def add_valid_luhn_checksum(number: str) -> str:
    """
    Добавляет валидную цифру к последовательности, так чтобы контрольная сумма была валидной.
    Алгоритм такой: приписываем справа 0, вычисляем контрольную сумму, затем вычитаем из 10 и приписываем получившуюся цифру.
    """
    checksum = calculate_luhn_checksum(number + "0")
    return number + str((10 - checksum ) % 10)
