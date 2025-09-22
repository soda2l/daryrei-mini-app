# 🚀 Быстрое исправление прав доступа

## ❌ Проблема: `Permission denied: 'catalog.json'`

На сервере у бота нет прав на запись в файл каталога.

## ⚡ Быстрое решение:

### **Вариант 1: Автоматически (рекомендуется)**
```bash
# Запусти этот файл локально
fix_server_permissions.bat
```

### **Вариант 2: Вручную на сервере**
```bash
# Подключись к серверу
ssh user@server

# Выполни эти команды
sudo chown -R www-data:www-data /var/www/daryrei-bot/
sudo chmod -R 755 /var/www/daryrei-bot/
sudo chmod 666 /var/www/daryrei-bot/catalog.json
sudo mkdir -p /var/www/daryrei-bot/images
sudo chmod 755 /var/www/daryrei-bot/images
sudo chown www-data:www-data /var/www/daryrei-bot/images
sudo systemctl restart daryrei-bot
```

## ✅ Проверка:

### **Проверь статус бота:**
```bash
sudo systemctl status daryrei-bot
```

### **Проверь логи:**
```bash
sudo journalctl -u daryrei-bot -f
```

### **Проверь API:**
```bash
curl https://daryreibot.duckdns.org/api/catalog
```

## 🎯 Результат:

После исправления:
- ✅ Товары добавляются без ошибок
- ✅ Фото загружаются и сохраняются
- ✅ Каталог обновляется корректно
- ✅ Админ-панель работает полностью

## 🔧 Если не помогло:

1. **Проверь свободное место:**
   ```bash
   df -h
   ```

2. **Проверь права на файл:**
   ```bash
   ls -la /var/www/daryrei-bot/catalog.json
   ```

3. **Перезапусти бота:**
   ```bash
   sudo systemctl restart daryrei-bot
   ```

4. **Проверь логи:**
   ```bash
   sudo journalctl -u daryrei-bot --since "1 hour ago"
   ```

## 📞 Готово!

Теперь бот должен работать без ошибок прав доступа! 🚀
