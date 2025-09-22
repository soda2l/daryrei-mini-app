# Обновление bot.py на сервере

## Проблема
API endpoint `/api/catalog` читает каталог из файла, а не из памяти бота, поэтому новые категории не появляются в мини-приложении.

## Решение

### 1. Подключись к серверу
```bash
ssh root@daryreibot.duckdns.org
```

### 2. Перейди в директорию бота
```bash
cd /var/www/daryrei-bot
```

### 3. Создай резервную копию
```bash
cp bot.py bot.py.backup
```

### 4. Отредактируй bot.py
Найди функцию `get_catalog()` в Flask API (около строки 162) и замени:

**Было:**
```python
@flask_app.route('/api/catalog', methods=['GET'])
def get_catalog():
    """API для получения каталога товаров"""
    try:
        # Читаем каталог напрямую из файла
        if os.path.exists(CATALOG_FILE):
            with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
                catalog = json.load(f)
        else:
            catalog = {"categories": [], "products": []}
        
        response = jsonify(catalog)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        logger.error(f"Ошибка при получении каталога: {e}")
        response = jsonify({"error": str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500
```

**Стало:**
```python
@flask_app.route('/api/catalog', methods=['GET'])
def get_catalog():
    """API для получения каталога товаров"""
    try:
        # Используем каталог из памяти бота (актуальная версия)
        catalog = self.get_catalog()
        
        response = jsonify(catalog)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        logger.error(f"Ошибка при получении каталога: {e}")
        response = jsonify({"error": str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500
```

### 5. Перезапусти бота
```bash
systemctl restart daryrei-bot
```

### 6. Проверь статус
```bash
systemctl status daryrei-bot
```

## Результат
После обновления новые категории, добавленные через бота, будут сразу появляться в мини-приложении.
