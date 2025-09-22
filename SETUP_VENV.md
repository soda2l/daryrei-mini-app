# Настройка виртуального окружения

## Проблема
```
error: externally-managed-environment
```

## Решение

### 1. Подключись к серверу
```bash
ssh root@147.45.164.202
```

### 2. Перейди в директорию бота
```bash
cd /var/www/daryrei-bot
```

### 3. Создай виртуальное окружение
```bash
python3 -m venv venv
```

### 4. Активируй виртуальное окружение
```bash
source venv/bin/activate
```

### 5. Установи зависимости
```bash
pip install python-telegram-bot flask requests
```

### 6. Проверь установку
```bash
python -c "import telegram, flask, requests; print('Все модули установлены успешно!')"
```

### 7. Обнови конфигурацию сервиса
```bash
nano /etc/systemd/system/daryrei-bot.service
```

Замени содержимое на:
```ini
[Unit]
Description=DaryRei Bot
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/daryrei-bot
ExecStart=/var/www/daryrei-bot/venv/bin/python /var/www/daryrei-bot/bot.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/var/www/daryrei-bot

[Install]
WantedBy=multi-user.target
```

### 8. Перезагрузи systemd
```bash
systemctl daemon-reload
```

### 9. Перезапусти сервис
```bash
systemctl restart daryrei-bot
```

### 10. Проверь статус
```bash
systemctl status daryrei-bot
```

## Альтернативный способ

Если не работает, попробуй установить через apt:
```bash
apt update
apt install python3-telegram-bot python3-flask python3-requests
```

## Проверка

После настройки виртуального окружения бот должен запуститься успешно.
