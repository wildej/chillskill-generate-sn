# Телеграм бот для генерации и проверки серийных номеров

Бот для генерации и проверки серийных номеров изделий в формате `XXSS-SSSS-SAAC`.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте файл `.env` на основе `.env.example` и укажите токен вашего бота:
```
BOT_TOKEN=your_bot_token_here
```

## Запуск

### Локальный запуск

```bash
python bot.py
```

### Запуск в Docker

#### Использование Docker Compose (рекомендуется)

1. Убедитесь, что файл `.env` создан и содержит токен бота
2. Запустите контейнер:
```bash
docker-compose up -d
```

3. Просмотр логов:
```bash
docker-compose logs -f
```

4. Остановка контейнера:
```bash
docker-compose down
```

#### Использование Docker напрямую

1. Соберите образ:
```bash
docker build -t telegram-serial-bot .
```

2. Запустите контейнер:
```bash
docker run -d --name telegram-serial-bot --env-file .env --restart unless-stopped telegram-serial-bot
```

3. Просмотр логов:
```bash
docker logs -f telegram-serial-bot
```

4. Остановка контейнера:
```bash
docker stop telegram-serial-bot
docker rm telegram-serial-bot
```

## Команды бота

### Генерация серийных номеров

- `/g` или `/generate` - генерирует 1 серийный номер
- `/g NN` или `/generate NN` - генерирует NN серийных номеров (максимум 10)

Каждый серийный номер отправляется в отдельном сообщении.

### Проверка серийного номера

- `/c XXXX-XXXX-XXXX` или `/check XXXX-XXXX-XXXX` - проверяет серийный номер

## Формат серийного номера

`XXSS-SSSS-SAAC`

- **XX** - номер квартала генерации (начиная с Q1 2026)
- **SSSSSSS** - уникальное число (секунды с начала квартала)
- **AA** - просто какие-то цифры
- **C** - контрольная сумма по алгоритму Луна

## Примеры использования

```
/g
/g 5
/c 0123-4567-8912
/check 012345678912
```
