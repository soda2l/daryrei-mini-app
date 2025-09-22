# Быстрое исправление systemd сервиса

## Проблема
```
Failed to spawn
Failed to start daryrei-bot.service
```

## Быстрое решение

### 1. Подключись к серверу
```bash
ssh root@147.45.164.202
```

### 2. Проверь конфигурацию сервиса
```bash
cat /etc/systemd/system/daryrei-bot.service
```

### 3. Если конфигурация неправильная, исправь её
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
ExecStart=/usr/bin/python3 /var/www/daryrei-bot/bot.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/var/www/daryrei-bot

[Install]
WantedBy=multi-user.target
```

### 4. Исправь права доступа
```bash
chown -R www-data:www-data /var/www/daryrei-bot
chmod +x /var/www/daryrei-bot/bot.py
```

### 5. Перезагрузи systemd
```bash
systemctl daemon-reload
```

### 6. Запусти сервис
```bash
systemctl start daryrei-bot
```

### 7. Проверь статус
```bash
systemctl status daryrei-bot
```

## Альтернативное решение

Если не работает, попробуй запустить бота напрямую:
```bash
cd /var/www/daryrei-bot
python3 bot.py
```

Это покажет реальную ошибку запуска.
