@echo off
echo Исправление ошибки 502 Bad Gateway...
echo.

echo 1. Копируем скрипт на сервер...
scp fix_server_502.sh user@server:/tmp/

echo.
echo 2. Запускаем скрипт на сервере...
ssh user@server "chmod +x /tmp/fix_server_502.sh && sudo /tmp/fix_server_502.sh"

echo.
echo 3. Проверяем API...
curl https://daryreibot.duckdns.org/api/catalog

echo.
echo ✅ Готово! Проверьте результат выше.
echo.
pause
