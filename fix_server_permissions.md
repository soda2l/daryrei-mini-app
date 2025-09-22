# 🔧 Исправление прав доступа на сервере

## ❌ Проблема: `Permission denied: 'catalog.json'`

На сервере у процесса бота нет прав на запись в файл `catalog.json`.

## ✅ Решение:

### **1. Подключись к серверу:**
```bash
ssh user@server
```

### **2. Перейди в папку бота:**
```bash
cd /var/www/daryrei-bot
```

### **3. Исправь права доступа:**
```bash
# Сделай владельцем папки пользователя www-data
sudo chown -R www-data:www-data /var/www/daryrei-bot/

# Дай права на чтение и запись
sudo chmod -R 755 /var/www/daryrei-bot/

# Особые права для файла каталога
sudo chmod 666 /var/www/daryrei-bot/catalog.json

# Создай папку для изображений если её нет
sudo mkdir -p /var/www/daryrei-bot/images
sudo chmod 755 /var/www/daryrei-bot/images
sudo chown www-data:www-data /var/www/daryrei-bot/images
```

### **4. Проверь права:**
```bash
ls -la /var/www/daryrei-bot/
ls -la /var/www/daryrei-bot/catalog.json
ls -la /var/www/daryrei-bot/images/
```

### **5. Перезапусти бота:**
```bash
sudo systemctl restart daryrei-bot
sudo systemctl status daryrei-bot
```

## 🔍 Проверка результата:

### **Проверь логи бота:**
```bash
sudo journalctl -u daryrei-bot -f
```

### **Проверь API:**
```bash
curl https://daryreibot.duckdns.org/api/catalog
```

### **Проверь права доступа:**
```bash
# Файл каталога должен быть доступен для записи
ls -la /var/www/daryrei-bot/catalog.json
# Должно показать: -rw-rw-rw- 1 www-data www-data

# Папка изображений должна быть доступна для записи
ls -la /var/www/daryrei-bot/images/
# Должно показать: drwxr-xr-x 2 www-data www-data
```

## 🚀 Альтернативное решение:

### **Если проблема повторяется:**

1. **Проверь, под каким пользователем запущен бот:**
   ```bash
   ps aux | grep python
   ```

2. **Измени владельца файлов на пользователя бота:**
   ```bash
   sudo chown -R $(whoami):$(whoami) /var/www/daryrei-bot/
   sudo chmod -R 755 /var/www/daryrei-bot/
   sudo chmod 666 /var/www/daryrei-bot/catalog.json
   ```

3. **Или создай файл каталога заново:**
   ```bash
   sudo touch /var/www/daryrei-bot/catalog.json
   sudo chown www-data:www-data /var/www/daryrei-bot/catalog.json
   sudo chmod 666 /var/www/daryrei-bot/catalog.json
   ```

## 📋 Что должно работать после исправления:

- ✅ Товары добавляются без ошибок
- ✅ Фото загружаются и сохраняются
- ✅ Каталог обновляется корректно
- ✅ API возвращает актуальные данные

## 🔧 Дополнительная диагностика:

### **Если все еще не работает:**

1. **Проверь свободное место на диске:**
   ```bash
   df -h
   ```

2. **Проверь права на папку:**
   ```bash
   ls -la /var/www/
   ```

3. **Проверь конфигурацию systemd:**
   ```bash
   cat /etc/systemd/system/daryrei-bot.service
   ```

4. **Проверь логи systemd:**
   ```bash
   sudo journalctl -u daryrei-bot --since "1 hour ago"
   ```

## 📞 Результат:

После исправления прав доступа:
- ✅ Бот может сохранять изменения в каталог
- ✅ Фото загружаются без ошибок
- ✅ Админ-панель работает полностью
- ✅ Мини-приложение получает актуальные данные
