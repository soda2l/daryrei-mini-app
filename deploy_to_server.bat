@echo off
echo 🚀 ДЕПЛОЙ DARYREI BOT НА СЕРВЕР
echo ================================

echo.
echo ⚠️  ВАЖНО: Убедитесь, что на сервере остановлен текущий бот!
echo.

echo 📦 Пушим изменения в репозиторий...
git push origin master

if %errorlevel% neq 0 (
    echo ❌ Ошибка при пуше в репозиторий
    pause
    exit /b 1
)

echo ✅ Изменения успешно запушены в репозиторий
echo.
echo 📋 Следующие шаги на сервере:
echo 1. Подключитесь к серверу: ssh root@5689543-ie62389.timeweb.cloud
echo 2. Остановите бота: sudo systemctl stop daryrei-bot.service
echo 3. Обновите код: cd /var/www/daryrei_bot && git pull origin master
echo 4. Перезапустите бота: sudo systemctl start daryrei-bot.service
echo 5. Проверьте статус: sudo systemctl status daryrei-bot.service
echo.
echo 📖 Подробная инструкция в файле DEPLOY_INSTRUCTIONS.md
echo.
pause
