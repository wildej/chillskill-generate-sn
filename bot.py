"""
Телеграм бот для генерации и проверки серийных номеров.
"""
import os
import random
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from serial_number import generate_serial_number, parse_serial_number, format_serial_number, parse_serial_number

# версия бота
VERSION = "0.0.3"

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
            if count > 100:
                await update.message.reply_text(
                    "Максимальное количество серийных номеров - 99. "
                    "Будет сгенерировано 99 номеров."
                )
                count = 99
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
    
    # Генерируем серийные номера
    # Сначала сгенерируем список из count разных случайных чисел от 1 до 100
    adds_list = random.sample(range(1, 100), count)
    for adds in adds_list:
        serial = generate_serial_number(now, adds)
        formatted_serial = format_serial_number(serial)
        
        # Отправляем каждый номер в отдельном сообщении
        await update.message.reply_text(f"`{formatted_serial}`", parse_mode="Markdown")


async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /c или /check.
    Проверяет серийный номер.
    """
    if not context.args:
        await update.message.reply_text(
            "Использование: /c XXXX-XXXX-XXXX или /check XXXX-XXXX-XXXX"
        )
        return
    
    # Объединяем аргументы (на случай если номер введен с пробелами)
    serial = " ".join(context.args)
    
    # Проверяем серийный номер
    is_valid, message = parse_serial_number(serial)
    
    if is_valid:
        # Если валидный, message содержит информацию о дате генерации
        formatted_serial = format_serial_number(parse_serial_number(serial))
        response = f"`{formatted_serial}`\nВалидный номер. Дата генерации: {message}"
    else:
        # Если невалидный, message содержит сообщение об ошибке
        response = f"`{serial}`\nНевалидный номер ({message})"
    
    await update.message.reply_text(response, parse_mode="Markdown")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start.
    Отправляет справку по использованию бота.
    """
    help_text = (
        "👋 Добро пожаловать!\n\n"
        "Этот бот позволяет генерировать и проверять серийные номера изделий в формате `XXSS-SSSS-SAAC`.\n\n"
        "*Доступные команды:*\n"
        "• `/g` или `/generate` — генерирует 1 серийный номер\n"
        "• `/g NN` или `/generate NN` — генерирует NN серийных номеров (максимум 100)\n"
        "• `/c XXXX-XXXX-XXXX` или `/check XXXX-XXXX-XXXX` — проверяет серийный номер\n\n"
        "*Примеры:*\n"
        "`/g`\n"
        "`/g 5`\n"
        "`/c 0123-4567-8912`\n"
        "`/check 012345678912`\n\n"
        f"Версия: {VERSION}\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")



def main() -> None:
    """Запуск бота."""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler(["start"], start_command))
    application.add_handler(CommandHandler(["g", "generate"], generate_command))
    application.add_handler(CommandHandler(["c", "check"], check_command))
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
