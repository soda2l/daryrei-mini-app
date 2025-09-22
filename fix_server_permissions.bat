@echo off
echo Исправление прав доступа на сервере...
echo.

echo 1. Копируем скрипт на сервер...
scp fix_permissions.sh user@server:/tmp/

echo.
echo 2. Запускаем скрипт на сервере...
ssh user@server "chmod +x /tmp/fix_permissions.sh && sudo /tmp/fix_permissions.sh"

echo.
echo 3. Проверяем статус бота...
ssh user@server "sudo systemctl status daryrei-bot --no-pager"

echo.
echo ✅ Готово! Проверьте логи бота:
echo ssh user@server "sudo journalctl -u daryrei-bot -f"
echo.
pause
