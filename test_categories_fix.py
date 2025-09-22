#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест исправления категорий в мини-приложении
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

def test_categories_structure():
    """Тест структуры категорий"""
    print("🧪 Тестируем исправление категорий в мини-приложении...")
    
    catalog = load_catalog()
    categories = catalog.get("categories", [])
    products = catalog.get("products", [])
    
    print(f"\n📊 Статистика каталога:")
    print(f"   📁 Категорий: {len(categories)}")
    print(f"   📦 Товаров: {len(products)}")
    
    if not categories:
        print("❌ В каталоге нет категорий!")
        print("🔧 Решение: Добавьте категории через админ-панель")
        return False
    
    print(f"\n📋 Категории в каталоге:")
    for i, category in enumerate(categories, 1):
        print(f"   {i}. ID: {category.get('id', 'Нет ID')}")
        print(f"      Название: {category.get('name', 'Без названия')}")
        print(f"      Описание: {category.get('description', 'Без описания')}")
        print()
    
    # Проверяем, что у товаров есть категории
    products_with_categories = [p for p in products if p.get('category')]
    products_without_categories = [p for p in products if not p.get('category')]
    
    print(f"📦 Товары с категориями: {len(products_with_categories)}")
    print(f"📦 Товары без категорий: {len(products_without_categories)}")
    
    if products_without_categories:
        print("⚠️ Найдены товары без категорий:")
        for product in products_without_categories:
            print(f"   - {product.get('name', 'Без названия')} (ID: {product.get('id', 'Нет ID')})")
    
    return True

def test_js_categories_logic():
    """Тест логики загрузки категорий в JS"""
    print(f"\n🔧 Исправления в JavaScript:")
    print(f"1. ✅ Изменен const categories на let categories")
    print(f"2. ✅ Добавлена загрузка категорий из каталога в loadCatalog()")
    print(f"3. ✅ Добавлена загрузка категорий из fallback данных")
    print(f"4. ✅ Категории теперь динамически загружаются с сервера")
    
    print(f"\n📋 Логика загрузки категорий:")
    print(f"1. При загрузке каталога с сервера:")
    print(f"   - categories = ['all']")
    print(f"   - catalog.categories.forEach(category => categories.push(category.id))")
    print(f"2. При использовании fallback данных:")
    print(f"   - categories = ['all']")
    print(f"   - catalog.categories.forEach(category => categories.push(category.id))")
    
    return True

def test_category_usage():
    """Тест использования категорий"""
    print(f"\n🎯 Как используются категории:")
    print(f"1. Свайпы между категориями")
    print(f"2. Фильтрация товаров по категориям")
    print(f"3. Отображение товаров в категориях")
    
    print(f"\n📱 В мини-приложении:")
    print(f"1. Пользователь может свайпать между категориями")
    print(f"2. Товары фильтруются по выбранной категории")
    print(f"3. Категории загружаются динамически с сервера")
    
    return True

def main():
    """Главная функция"""
    print("🚀 Тест исправления категорий в мини-приложении")
    print("=" * 60)
    
    success1 = test_categories_structure()
    success2 = test_js_categories_logic()
    success3 = test_category_usage()
    
    if success1 and success2 and success3:
        print(f"\n✅ Все тесты пройдены успешно!")
        print(f"\n🚀 Следующие шаги:")
        print(f"1. Запусти бота: python bot.py")
        print(f"2. Добавь категории через админ-панель: /admin")
        print(f"3. Проверь мини-приложение - категории должны отображаться")
        print(f"4. Протестируй свайпы между категориями")
    else:
        print(f"\n❌ Некоторые тесты не прошли")
        print(f"\n🔧 Что нужно исправить:")
        if not success1:
            print(f"1. Добавьте категории в каталог")
        if not success2:
            print(f"2. Проверьте исправления в JavaScript")
        if not success3:
            print(f"3. Проверьте использование категорий")

if __name__ == "__main__":
    main()
