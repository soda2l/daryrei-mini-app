# Исправление ошибки запуска бота

## Проблема
```
Job for daryrei-bot.service failed because of unavailable resources or another system error.
```

## Диагностика

### 1. Подключись к серверу
```bash
ssh root@147.45.164.202
```

### 2. Проверь статус сервиса
```bash
systemctl status daryrei-bot.service
```

### 3. Проверь логи
```bash
journalctl -xeu daryrei-bot.service -n 20
```

### 4. Проверь синтаксис Python
```bash
cd /var/www/daryrei-bot
python3 -m py_compile bot.py
```

### 5. Проверь зависимости
```bash
cd /var/www/daryrei-bot
python3 -c "import telegram, flask, requests"
```

## Возможные причины и решения

### 1. Синтаксическая ошибка в bot.py
**Решение:** Исправь ошибку в коде
```bash
nano bot.py
```

### 2. Отсутствуют зависимости
**Решение:** Установи зависимости
```bash
pip3 install python-telegram-bot flask requests
```

### 3. Неправильные права доступа
**Решение:** Исправь права
```bash
chown -R www-data:www-data /var/www/daryrei-bot
chmod -R 755 /var/www/daryrei-bot
```

### 4. Порт 8000 занят
**Решение:** Проверь, что порт свободен
```bash
netstat -tlnp | grep :8000
```

### 5. Проблема с переменными окружения
**Решение:** Проверь, что BOT_TOKEN установлен
```bash
echo $BOT_TOKEN
```

## После исправления

### Перезапусти бота
```bash
systemctl restart daryrei-bot
```

### Проверь статус
```bash
systemctl status daryrei-bot
```
