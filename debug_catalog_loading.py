#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диагностика проблемы с загрузкой каталога
"""

import requests
import json
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Конфигурация
SERVER_API_URL = "https://daryreibot.duckdns.org/api/catalog"

def test_server_api():
    """Тест API сервера"""
    print("🌐 Тестируем API сервера...")
    
    try:
        response = requests.get(SERVER_API_URL, timeout=10)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            catalog = response.json()
            print("✅ API сервера работает")
            
            # Проверяем структуру каталога
            print(f"\n📊 Структура каталога:")
            print(f"   Ключи: {list(catalog.keys())}")
            
            # Проверяем категории
            categories = catalog.get('categories', [])
            print(f"\n📁 Категории ({len(categories)}):")
            for i, category in enumerate(categories, 1):
                print(f"   {i}. ID: {category.get('id', 'Нет ID')}")
                print(f"      Название: {category.get('name', 'Без названия')}")
                print()
            
            # Проверяем товары
            products = catalog.get('products', [])
            print(f"📦 Товары ({len(products)}):")
            for i, product in enumerate(products[:3], 1):  # Показываем первые 3
                print(f"   {i}. ID: {product.get('id', 'Нет ID')}")
                print(f"      Название: {product.get('name', 'Без названия')}")
                print(f"      Категория: {product.get('category', 'Без категории')}")
                print(f"      Цена: {product.get('price', 'Без цены')} ₽")
                print(f"      Описание: {product.get('description', 'Без описания')[:50]}...")
                print()
            
            return catalog
        else:
            print(f"❌ Ошибка API: HTTP {response.status_code}")
            print(f"Ответ: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Ошибка при обращении к API: {e}")
        return None

def test_fallback_data():
    """Тест fallback данных"""
    print("\n💾 Тестируем fallback данные...")
    
    # Симулируем fallback данные
    fallback_catalog = {
        "categories": [
            { "id": "candles", "name": "Свечи" },
            { "id": "boxes", "name": "Коробки" },
            { "id": "postcards", "name": "Открытки" },
            { "id": "stickers", "name": "Стикеры" },
            { "id": "home", "name": "Для дома" }
        ],
        "products": [
            {
                "id": "candle_banana_chocolate",
                "name": "Свеча \"Банан-шоколад\"",
                "category": "candles",
                "price": 1290,
                "description": "Состав набора: 🧦🎧⛈️ свеча с ароматом «банан в овсяном молоке, теплого какао с душистыми нотами натуральных кофейных зерен», гипсовое кашпо цвета топленого молока с матовой текстурой, чем-то напоминающей старинный фарфор, подарочная упаковка, уютные подарочки 🌧️ 🍪☕️ 🍌",
                "images": ["candle_банан_шоколад.jpg"],
                "available": True
            }
        ]
    }
    
    print("✅ Fallback данные созданы")
    print(f"   Категорий: {len(fallback_catalog['categories'])}")
    print(f"   Товаров: {len(fallback_catalog['products'])}")
    
    return fallback_catalog

def main():
    """Главная функция"""
    print("🔍 Диагностика проблемы с загрузкой каталога")
    print("=" * 50)
    
    # Тестируем API сервера
    server_catalog = test_server_api()
    
    # Тестируем fallback данные
    fallback_catalog = test_fallback_data()
    
    print("\n📋 Рекомендации:")
    
    if not server_catalog:
        print("1. ❌ Сервер недоступен - используйте fallback данные")
        print("2. 🔧 Проверьте, что бот запущен на сервере")
        print("3. 🌐 Проверьте URL сервера")
    else:
        print("1. ✅ Сервер доступен")
        print("2. 🔄 Синхронизируйте каталог с сервера")
    
    print("\n🚀 Следующие шаги:")
    print("1. Проверьте консоль браузера (F12) на ошибки")
    print("2. Убедитесь, что сервер возвращает валидный JSON")
    print("3. Проверьте, что fallback данные работают")

if __name__ == "__main__":
    main()
