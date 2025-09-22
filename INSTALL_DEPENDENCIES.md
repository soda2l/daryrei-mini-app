# Установка зависимостей Python

## Проблема
```
ModuleNotFoundError: No module named 'telegram'
```

## Решение

### 1. Подключись к серверу
```bash
ssh root@147.45.164.202
```

### 2. Установи зависимости
```bash
pip3 install python-telegram-bot
pip3 install flask
pip3 install requests
```

### 3. Проверь установку
```bash
python3 -c "import telegram, flask, requests; print('Все модули установлены успешно!')"
```

### 4. Перезапусти сервис
```bash
systemctl restart daryrei-bot
```

### 5. Проверь статус
```bash
systemctl status daryrei-bot
```

## Альтернативный способ

Если pip3 не работает, попробуй:
```bash
apt update
apt install python3-pip
pip3 install python-telegram-bot flask requests
```

## Проверка

После установки зависимостей бот должен запуститься без ошибок.
