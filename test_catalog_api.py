#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест API каталога для проверки категорий
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
LOCAL_CATALOG_FILE = "catalog.json"

def test_server_api():
    """Тест API сервера"""
    print("🌐 Тестируем API сервера...")
    
    try:
        response = requests.get(SERVER_API_URL, timeout=10)
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
                print(f"      Описание: {category.get('description', 'Без описания')}")
                print()
            
            # Проверяем товары
            products = catalog.get('products', [])
            print(f"📦 Товары ({len(products)}):")
            for i, product in enumerate(products[:5], 1):  # Показываем первые 5
                print(f"   {i}. ID: {product.get('id', 'Нет ID')}")
                print(f"      Название: {product.get('name', 'Без названия')}")
                print(f"      Категория: {product.get('category', 'Без категории')}")
                print(f"      Цена: {product.get('price', 'Без цены')} ₽")
                print()
            
            return catalog
        else:
            print(f"❌ Ошибка API: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Ошибка при обращении к API: {e}")
        return None

def test_local_catalog():
    """Тест локального каталога"""
    print("\n💾 Тестируем локальный каталог...")
    
    try:
        with open(LOCAL_CATALOG_FILE, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
        
        print("✅ Локальный каталог загружен")
        
        # Проверяем структуру каталога
        print(f"\n📊 Структура каталога:")
        print(f"   Ключи: {list(catalog.keys())}")
        
        # Проверяем категории
        categories = catalog.get('categories', [])
        print(f"\n📁 Категории ({len(categories)}):")
        for i, category in enumerate(categories, 1):
            print(f"   {i}. ID: {category.get('id', 'Нет ID')}")
            print(f"      Название: {category.get('name', 'Без названия')}")
            print(f"      Описание: {category.get('description', 'Без описания')}")
            print()
        
        return catalog
    except Exception as e:
        print(f"❌ Ошибка при загрузке локального каталога: {e}")
        return None

def compare_catalogs(server_catalog, local_catalog):
    """Сравнить каталоги"""
    print("\n🔄 Сравниваем каталоги...")
    
    if not server_catalog or not local_catalog:
        print("❌ Не удалось сравнить каталоги")
        return
    
    server_categories = {c['id']: c for c in server_catalog.get('categories', [])}
    local_categories = {c['id']: c for c in local_catalog.get('categories', [])}
    
    print(f"📊 Статистика категорий:")
    print(f"   На сервере: {len(server_categories)}")
    print(f"   Локально: {len(local_categories)}")
    
    # Проверяем различия
    server_only = set(server_categories.keys()) - set(local_categories.keys())
    local_only = set(local_categories.keys()) - set(server_categories.keys())
    
    if server_only:
        print(f"   Только на сервере: {len(server_only)}")
    if local_only:
        print(f"   Только локально: {len(local_only)}")
    
    if not server_only and not local_only:
        print("   ✅ Категории синхронизированы")
    else:
        print("   ⚠️ Есть различия в категориях")

def main():
    """Главная функция"""
    print("🧪 Тест API каталога для проверки категорий")
    print("=" * 50)
    
    # Тестируем API сервера
    server_catalog = test_server_api()
    
    # Тестируем локальный каталог
    local_catalog = test_local_catalog()
    
    # Сравниваем каталоги
    if server_catalog and local_catalog:
        compare_catalogs(server_catalog, local_catalog)
    
    print("\n📋 Рекомендации:")
    
    if not server_catalog:
        print("1. ❌ API сервера недоступен - проверьте интернет-соединение")
        print("2. 🔧 Проверьте, что бот запущен на сервере")
        print("3. 🌐 Проверьте URL сервера")
    
    if not local_catalog:
        print("1. 💾 Локальный каталог не найден")
        print("2. 🔄 Синхронизируйте с сервером")
    
    if server_catalog and local_catalog:
        server_categories = len(server_catalog.get('categories', []))
        local_categories = len(local_catalog.get('categories', []))
        
        if server_categories == 0:
            print("1. ❌ На сервере нет категорий")
            print("2. 🔧 Добавьте категории через админ-панель")
            print("3. 🔄 Синхронизируйте каталог")
        
        if local_categories == 0:
            print("1. ❌ Локально нет категорий")
            print("2. 🔄 Синхронизируйте с сервером")
    
    print("\n🚀 Следующие шаги:")
    print("1. Запустите sync_catalog.bat для синхронизации")
    print("2. Проверьте, что категории добавлены через админ-панель")
    print("3. Убедитесь, что мини-приложение загружает данные с сервера")

if __name__ == "__main__":
    main()
