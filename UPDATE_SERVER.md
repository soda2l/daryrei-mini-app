# 🔧 Обновление бота на сервере

## ❌ Проблема:
Бот падает с ошибкой `AttributeError: 'DaryReiBot' object has no attribute 'test_webapp_data_command'`

## ✅ Решение:
Исправлена ошибка в коде - удалена ссылка на несуществующий метод.

## 🚀 Инструкции по обновлению:

### 1. Подключись к серверу:
```bash
ssh root@5689543-ie62389
```

### 2. Перейди в папку проекта:
```bash
cd /var/www/daryrei-bot
```

### 3. Останови бота:
```bash
systemctl stop daryrei-bot
```

### 4. Обнови код:
```bash
git pull origin master
```

### 5. Запусти бота:
```bash
systemctl start daryrei-bot
```

### 6. Проверь статус:
```bash
systemctl status daryrei-bot
```

### 7. Посмотри логи (если нужно):
```bash
journalctl -u daryrei-bot.service -f
```

## 🔍 Альтернативный способ (если git pull не работает):

### 1. Создай резервную копию:
```bash
cp bot.py bot.py.backup
```

### 2. Отредактируй файл:
```bash
nano bot.py
```

### 3. Найди строку 64 и удали её:
```python
# Удали эту строку:
self.application.add_handler(CommandHandler("testwebapp", self.test_webapp_data_command))
```

### 4. Сохрани файл (Ctrl+X, Y, Enter)

### 5. Перезапусти бота:
```bash
systemctl restart daryrei-bot
```

## ✅ Проверка:
После обновления бот должен запуститься без ошибок и работать корректно.

## 📞 Если проблемы остаются:
Проверь логи командой:
```bash
journalctl -u daryrei-bot.service -n 50
```
