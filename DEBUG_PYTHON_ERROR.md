# Диагностика ошибки Python скрипта

## Проблема
```
Process: 26014 ExecStart=/usr/bin/python3 /var/www/daryrei-bot/bot.py (code=exited, status=1/FAILURE)
```

## Диагностика

### 1. Подключись к серверу
```bash
ssh root@147.45.164.202
```

### 2. Запусти bot.py напрямую для диагностики
```bash
cd /var/www/daryrei-bot
python3 bot.py
```

Это покажет реальную ошибку Python.

### 3. Проверь синтаксис Python
```bash
cd /var/www/daryrei-bot
python3 -m py_compile bot.py
```

### 4. Проверь зависимости
```bash
cd /var/www/daryrei-bot
python3 -c "import telegram, flask, requests"
```

### 5. Проверь переменные окружения
```bash
echo $BOT_TOKEN
echo $ORDER_GROUP_ID
```

## Возможные причины и решения

### 1. Отсутствует BOT_TOKEN
**Решение:** Установи переменную окружения
```bash
export BOT_TOKEN="твой_токен_бота"
```

### 2. Отсутствуют зависимости
**Решение:** Установи зависимости
```bash
pip3 install python-telegram-bot flask requests
```

### 3. Синтаксическая ошибка в bot.py
**Решение:** Исправь ошибку в коде

### 4. Проблема с правами доступа
**Решение:** Исправь права
```bash
chown -R www-data:www-data /var/www/daryrei-bot
chmod +x /var/www/daryrei-bot/bot.py
```

### 5. Порт 8000 занят
**Решение:** Проверь, что порт свободен
```bash
netstat -tlnp | grep :8000
```

## После исправления

### Перезапусти сервис
```bash
systemctl restart daryrei-bot
```

### Проверь статус
```bash
systemctl status daryrei-bot
```
