"""
Телеграм бот для генерации и проверки серийных номеров.
"""
import os
import random
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from serial_number import generate_serial_number, validate_serial_number, Q1_2026_START

# Загружаем переменные окружения
load_dotenv()

# Токен бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен в переменных окружения!")


async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /g или /generate.
    Генерирует серийные номера.
    """
    # Определяем количество серийников для генерации
    count = 1
    if context.args:
        try:
            count = int(context.args[0])
            if count > 10:
                await update.message.reply_text(
                    "Максимальное количество серийных номеров - 10. "
                    "Будет сгенерировано 10 номеров."
                )
                count = 10
            elif count < 1:
                await update.message.reply_text(
                    "Количество должно быть положительным числом. "
                    "Будет сгенерирован 1 номер."
                )
                count = 1
        except ValueError:
            count = 1
    
    # Получаем текущее время один раз
    from datetime import datetime, timezone
    
    now = datetime.now(timezone.utc)
    start_timestamp = Q1_2026_START.timestamp()
    current_timestamp = now.timestamp()
    base_timestamp_ms = int((current_timestamp - start_timestamp) * 1000)
    
    # Генерируем серийные номера
    offset = 0
    for i in range(count):
        offset = offset + random.randint(1, 100)
        serial = generate_serial_number(base_timestamp_ms, offset)
        
        # Отправляем каждый номер в отдельном сообщении
        await update.message.reply_text(f"`{serial}`", parse_mode="Markdown")


async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /c или /check.
    Проверяет серийный номер.
    """
    if not context.args:
        await update.message.reply_text(
            "Использование: /c XX-YYYY-YYYY-YYYZ или /check XX-YYYY-YYYY-YYYZ"
        )
        return
    
    # Объединяем аргументы (на случай если номер введен с пробелами)
    serial = " ".join(context.args)
    
    # Проверяем серийный номер
    is_valid, error_message, generation_date = validate_serial_number(serial)
    
    if is_valid:
        response = f"`{serial}`\nВалидный номер. Дата генерации: {generation_date}"
    else:
        response = f"`{serial}`\nНевалидный номер"
        if error_message:
            response += f" ({error_message})"
    
    await update.message.reply_text(response, parse_mode="Markdown")


def main() -> None:
    """Запуск бота."""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler(["g", "generate"], generate_command))
    application.add_handler(CommandHandler(["c", "check"], check_command))
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
