# 🔧 Исправление ошибки 502 Bad Gateway

## ❌ Проблема: 502 Bad Gateway

Сервер nginx работает, но не может подключиться к боту. Это означает, что:
- nginx запущен ✅
- Бот не запущен или не отвечает ❌
- Проблема с конфигурацией nginx ❌

## ✅ Решения:

### **Вариант 1: Перезапустить бота на сервере**
```bash
# Подключись к серверу
ssh user@server

# Проверь статус бота
sudo systemctl status daryrei-bot

# Перезапусти бота
sudo systemctl restart daryrei-bot

# Проверь логи
sudo journalctl -u daryrei-bot -f
```

### **Вариант 2: Проверить конфигурацию nginx**
```bash
# Проверь конфигурацию nginx
sudo nginx -t

# Перезапусти nginx
sudo systemctl restart nginx

# Проверь статус
sudo systemctl status nginx
```

### **Вариант 3: Проверить порты**
```bash
# Проверь, что бот слушает порт 8000
netstat -tlnp | grep 8000

# Проверь, что nginx проксирует на порт 8000
cat /etc/nginx/sites-available/daryrei-bot
```

## 🚀 Быстрое исправление:

### **Шаг 1: Подключись к серверу**
```bash
ssh user@server
```

### **Шаг 2: Проверь статус бота**
```bash
sudo systemctl status daryrei-bot
```

### **Шаг 3: Перезапусти бота**
```bash
sudo systemctl restart daryrei-bot
```

### **Шаг 4: Проверь логи**
```bash
sudo journalctl -u daryrei-bot --since "5 minutes ago"
```

### **Шаг 5: Проверь API**
```bash
curl http://localhost:8000/api/catalog
```

## 🔍 Диагностика:

### **Если бот не запускается:**
```bash
# Проверь права доступа
sudo chown -R www-data:www-data /var/www/daryrei-bot/
sudo chmod -R 755 /var/www/daryrei-bot/

# Проверь зависимости
cd /var/www/daryrei-bot/
source venv/bin/activate
pip install -r requirements.txt

# Запусти бота вручную
python bot.py
```

### **Если nginx не проксирует:**
```bash
# Проверь конфигурацию
cat /etc/nginx/sites-available/daryrei-bot

# Должно быть:
# location /api/ {
#     proxy_pass http://localhost:8000;
# }
```

## 📋 Проверка результата:

### **После исправления:**
```bash
# Проверь API
curl https://daryreibot.duckdns.org/api/catalog

# Должен вернуть JSON с каталогом
```

### **В мини-приложении:**
- Каталог загружается быстро
- Товары отображаются с новыми описаниями
- Категории работают корректно

## 🎯 Результат:

После исправления:
- ✅ API сервера работает (статус 200)
- ✅ Каталог загружается с сервера
- ✅ Мини-приложение работает быстро
- ✅ Fallback данные как резерв

## 🚀 Следующие шаги:

1. **Исправь проблему на сервере** (выбери один из вариантов выше)
2. **Проверь API** - должен вернуть JSON
3. **Протестируй мини-приложение** - должно загружаться быстро
4. **Убедись, что товары отображаются** с новыми описаниями

Готово! 🎉
