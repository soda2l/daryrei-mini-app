#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_catalog_api():
    """Тестируем API каталога"""
    print("🔄 Тестируем API каталога...")
    
    try:
        response = requests.get("http://localhost:8000/api/catalog")
        if response.status_code == 200:
            catalog = response.json()
            print(f"✅ API каталога работает")
            print(f"📦 Товаров: {len(catalog.get('products', []))}")
            print(f"📁 Категорий: {len(catalog.get('categories', []))}")
            return True
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def test_health_api():
    """Тестируем API здоровья"""
    print("🔄 Тестируем API здоровья...")
    
    try:
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ API здоровья работает: {health.get('message')}")
            return True
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def test_image_api():
    """Тестируем API изображений"""
    print("🔄 Тестируем API изображений...")
    
    try:
        response = requests.get("http://localhost:8000/images/candle_банан_шоколад.jpg")
        if response.status_code == 200:
            print(f"✅ API изображений работает")
            return True
        else:
            print(f"❌ Ошибка API изображений: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def main():
    print("🧪 ТЕСТИРОВАНИЕ АДМИН-ПАНЕЛИ DARYREI BOT")
    print("=" * 50)
    
    # Тестируем все API
    health_ok = test_health_api()
    catalog_ok = test_catalog_api()
    image_ok = test_image_api()
    
    print("\n📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"🏥 API здоровья: {'✅' if health_ok else '❌'}")
    print(f"📦 API каталога: {'✅' if catalog_ok else '❌'}")
    print(f"🖼️ API изображений: {'✅' if image_ok else '❌'}")
    
    if all([health_ok, catalog_ok, image_ok]):
        print("\n🎉 Все тесты пройдены! Админ-панель готова к работе.")
        print("\n📋 Доступные команды для тестирования в Telegram:")
        print("• /admin - Открыть админ-панель")
        print("• /add_product - Добавить товар")
        print("• /add_category - Добавить категорию")
        print("• /list_products - Показать товары")
        print("• /list_categories - Показать категории")
        print("• /reset - Сбросить состояния")
    else:
        print("\n⚠️ Некоторые тесты не пройдены. Проверьте логи бота.")

if __name__ == "__main__":
    main()
