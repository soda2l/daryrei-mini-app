# 🔧 Настройка прав доступа на сервере

## 🚨 Критически важные права

### 1. **Файл каталога (catalog.json)**
```bash
chmod 666 /var/www/daryrei_bot/catalog.json
```
**Почему:** Бот должен иметь возможность читать и записывать в этот файл.

### 2. **Каталог изображений**
```bash
chmod 755 /var/www/daryrei_bot/images/
chmod 644 /var/www/daryrei_bot/images/*
```
**Почему:** Flask должен иметь доступ к изображениям для отображения в мини-приложении.

### 3. **Основной файл бота**
```bash
chmod 755 /var/www/daryrei_bot/bot.py
```
**Почему:** Файл должен быть исполняемым.

## 📋 Полная настройка прав

### Вариант 1: Автоматический скрипт
```bash
# На сервере
cd /var/www/daryrei_bot
chmod +x setup_permissions.sh
./setup_permissions.sh
```

### Вариант 2: Быстрое исправление
```bash
# На сервере
cd /var/www/daryrei_bot
chmod +x fix_permissions_quick.sh
./fix_permissions_quick.sh
```

### Вариант 3: Ручная настройка
```bash
# На сервере
cd /var/www/daryrei_bot

# Основные права
chmod 755 .
chmod 644 *.py *.json *.html *.md
chmod +x bot.py

# Каталог изображений
chmod 755 images/
chmod 644 images/*

# Критически важные файлы
chmod 666 catalog.json

# Проверка
ls -la catalog.json
ls -la images/
```

## 🔍 Проверка прав

### Проверьте следующие файлы:
```bash
# Файл каталога (должен быть 666)
ls -la catalog.json
# Ожидаемый результат: -rw-rw-rw-

# Каталог изображений (должен быть 755)
ls -la images/
# Ожидаемый результат: drwxr-xr-x

# Основной файл бота (должен быть 755)
ls -la bot.py
# Ожидаемый результат: -rwxr-xr-x
```

## ⚠️ Частые проблемы

### 1. **Permission denied: 'catalog.json'**
```bash
chmod 666 catalog.json
```

### 2. **Изображения не загружаются**
```bash
chmod 755 images/
chmod 644 images/*
```

### 3. **Бот не запускается**
```bash
chmod +x bot.py
```

### 4. **Flask не может читать файлы**
```bash
chmod 644 *.py *.json *.html
```

## 🚀 После настройки прав

1. **Перезапустите бота:**
```bash
sudo systemctl restart daryrei-bot
```

2. **Проверьте статус:**
```bash
sudo systemctl status daryrei-bot
```

3. **Проверьте логи:**
```bash
sudo journalctl -u daryrei-bot -f
```

## 📝 Дополнительные настройки

### Если используете systemd:
```bash
# Создайте файл сервиса
sudo nano /etc/systemd/system/daryrei-bot.service
```

Содержимое файла:
```ini
[Unit]
Description=DaryRei Telegram Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/daryrei_bot
ExecStart=/usr/bin/python3 /var/www/daryrei_bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Активация сервиса:
```bash
sudo systemctl daemon-reload
sudo systemctl enable daryrei-bot
sudo systemctl start daryrei-bot
```

## ✅ Итоговая проверка

После настройки всех прав:
1. ✅ `catalog.json` имеет права 666
2. ✅ `images/` имеет права 755
3. ✅ `bot.py` исполняемый (755)
4. ✅ Все Python файлы читаемые (644)
5. ✅ Бот запускается без ошибок
6. ✅ Мини-приложение загружает изображения
7. ✅ Админ-панель работает корректно
