# Отключаем pager для git
$env:GIT_PAGER = ""

# Показываем текущую ветку
Write-Host "Текущая ветка:"
git branch --show-current

# Переключаемся на ветку main
Write-Host "Переключаемся на ветку main..."
git checkout main

# Показываем статус
Write-Host "Статус после переключения:"
git status

Write-Host "Готово! Теперь ты на ветке main."
