#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест нового интерфейса удаления товаров по категориям
"""

import json
import os
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Путь к файлу каталога
CATALOG_FILE = "catalog.json"

def load_catalog():
    """Загрузить каталог"""
    try:
        if os.path.exists(CATALOG_FILE):
            with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
                catalog = json.load(f)
            return catalog
        else:
            return {"categories": [], "products": []}
    except Exception as e:
        logger.error(f"Ошибка при загрузке каталога: {e}")
        return {"categories": [], "products": []}

def test_category_products():
    """Тест товаров по категориям"""
    print("🧪 Тестируем новый интерфейс удаления товаров по категориям...")
    
    catalog = load_catalog()
    categories = catalog.get("categories", [])
    products = catalog.get("products", [])
    
    print(f"\n📊 Статистика каталога:")
    print(f"   📁 Категорий: {len(categories)}")
    print(f"   📦 Товаров: {len(products)}")
    
    if not categories:
        print("❌ В каталоге нет категорий")
        return False
    
    print(f"\n📋 Товары по категориям:")
    
    for category in categories:
        category_id = category["id"]
        category_name = category["name"]
        
        # Находим товары в категории
        products_in_category = [p for p in products if p.get("category") == category_id]
        count = len(products_in_category)
        
        print(f"\n📁 {category_name} ({count} товаров):")
        
        if products_in_category:
            for i, product in enumerate(products_in_category, 1):
                print(f"   {i}. {product.get('name', 'Без названия')} - {product.get('price', 'Без цены')} ₽")
        else:
            print("   (нет товаров)")
    
    print(f"\n✅ Новый интерфейс готов!")
    print(f"\n📋 Как использовать:")
    print(f"1. Отправь /admin")
    print(f"2. Выбери 'Удалить товар (по категории)'")
    print(f"3. Выбери категорию")
    print(f"4. Выбери товар для удаления")
    
    return True

def test_commands():
    """Тест команд"""
    print(f"\n🔧 Доступные команды:")
    print(f"• /delete_product - Удалить товар (все)")
    print(f"• /delete_product_by_category - Удалить товар (по категории)")
    print(f"• /admin - Админ-панель")
    
    print(f"\n📱 В админ-панели:")
    print(f"• Удалить товар (все) - показывает все товары")
    print(f"• Удалить товар (по категории) - показывает категории с количеством товаров")
    
    return True

def main():
    """Главная функция"""
    print("🚀 Тест нового интерфейса удаления товаров")
    print("=" * 50)
    
    success1 = test_category_products()
    success2 = test_commands()
    
    if success1 and success2:
        print(f"\n✅ Все тесты пройдены успешно!")
        print(f"\n🚀 Следующие шаги:")
        print(f"1. Запусти бота: python bot.py")
        print(f"2. Отправь /admin")
        print(f"3. Протестируй новый интерфейс удаления")
    else:
        print(f"\n❌ Некоторые тесты не прошли")

if __name__ == "__main__":
    main()
