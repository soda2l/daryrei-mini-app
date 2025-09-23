# 🚀 Инструкция по деплою на сервер

## ⚠️ ВАЖНО: Перед деплоем

### 1. Остановите текущий бот на сервере
```bash
# Подключитесь к серверу
ssh root@5689543-ie62389.timeweb.cloud

# Остановите сервис
sudo systemctl stop daryrei-bot.service

# Проверьте, что процесс остановлен
ps aux | grep python
```

### 2. Сделайте бэкап текущего состояния
```bash
# На сервере
cd /var/www/daryrei_bot
cp -r . ../daryrei_bot_backup_$(date +%Y%m%d_%H%M%S)
```

## 📦 Деплой изменений

### 1. Запушьте изменения
```bash
# На локальной машине
git push origin master
```

### 2. Обновите код на сервере
```bash
# На сервере
cd /var/www/daryrei_bot
git pull origin master
```

### 3. Установите новые зависимости (если нужно)
```bash
# На сервере
pip install -r requirements.txt
```

### 4. Обновите мини-приложение
```bash
# На сервере - обновите index.html с правильными URL
# Замените localhost:8000 на daryreibot.duckdns.org
```

### 5. Перезапустите сервис
```bash
# На сервере
sudo systemctl start daryrei-bot.service
sudo systemctl status daryrei-bot.service
```

## 🔧 Проверка работы

### 1. Проверьте API
```bash
curl https://daryreibot.duckdns.org/api/health
curl https://daryreibot.duckdns.org/api/catalog
```

### 2. Проверьте изображения
```bash
curl https://daryreibot.duckdns.org/images/candle_банан_шоколад.jpg
```

### 3. Проверьте логи
```bash
sudo journalctl -u daryrei-bot.service -f
```

## 🐛 Если что-то пошло не так

### Откат к предыдущей версии
```bash
# На сервере
cd /var/www/daryrei_bot
git reset --hard HEAD~1
sudo systemctl restart daryrei-bot.service
```

### Или восстановите из бэкапа
```bash
# На сервере
cd /var/www
rm -rf daryrei_bot
mv daryrei_bot_backup_* daryrei_bot
cd daryrei_bot
sudo systemctl start daryrei-bot.service
```

## 📋 Что изменилось

### ✅ Новые возможности:
- Команда `/reset` для сброса состояний
- Кнопки быстрого доступа в админ-панели
- Поддержка статических изображений
- Улучшенная обработка ошибок

### 🔧 Технические улучшения:
- Добавлен маршрут `/images/<filename>` в Flask API
- Улучшена админ-панель с интерактивными кнопками
- Добавлены инструменты тестирования

## 🎯 После деплоя

1. **Протестируйте админ-панель:**
   - Отправьте `/admin` боту
   - Попробуйте добавить товар
   - Проверьте сброс состояний

2. **Проверьте мини-приложение:**
   - Откройте магазин через бота
   - Убедитесь, что изображения загружаются
   - Протестируйте оформление заказа

3. **Мониторинг:**
   - Следите за логами первые 30 минут
   - Проверьте, что нет ошибок 409 Conflict

## 🆘 Поддержка

Если возникли проблемы:
1. Проверьте логи: `sudo journalctl -u daryrei-bot.service -n 50`
2. Проверьте статус: `sudo systemctl status daryrei-bot.service`
3. Перезапустите: `sudo systemctl restart daryrei-bot.service`
