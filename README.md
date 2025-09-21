# DaryRei Bot

Telegram бот для обработки заказов из мини-приложения.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте файл `.env` с переменными окружения:
```
BOT_TOKEN=your_bot_token_here
ORDER_GROUP_ID=your_group_id_here
```

3. Запустите бота:
```bash
python bot.py
```

## API

- `GET /api/health` - проверка статуса
- `POST /api/order` - отправка заказа в группу

## Переменные окружения

- `BOT_TOKEN` - токен Telegram бота
- `ORDER_GROUP_ID` - ID группы для получения заказов
