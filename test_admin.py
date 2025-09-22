#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import os

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Путь к файлу каталога
CATALOG_FILE = "catalog.json"

def test_catalog_operations():
    """Тест операций с каталогом"""
    print("Тестируем операции с каталогом...")
    
    # Загружаем каталог
    try:
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
        print("✅ Каталог загружен успешно")
    except Exception as e:
        print(f"❌ Ошибка загрузки каталога: {e}")
        return
    
    # Проверяем структуру
    if "categories" not in catalog:
        print("❌ Нет поля 'categories' в каталоге")
        return
    if "products" not in catalog:
        print("❌ Нет поля 'products' в каталоге")
        return
    
    print("✅ Структура каталога корректна")
    
    # Показываем статистику
    categories_count = len(catalog.get("categories", []))
    products_count = len(catalog.get("products", []))
    
    print(f"📁 Категорий: {categories_count}")
    print(f"📦 Товаров: {products_count}")
    
    # Показываем категории
    print("\n📁 Категории:")
    for category in catalog.get("categories", []):
        print(f"  - {category.get('name', 'Без названия')} (ID: {category.get('id', 'Нет ID')})")
    
    # Показываем первые 3 товара
    print("\n📦 Товары:")
    for i, product in enumerate(catalog.get("products", [])[:3], 1):
        print(f"  {i}. {product.get('name', 'Без названия')} - {product.get('price', 0)} ₽")
    
    print("\n✅ Тест завершен успешно!")

if __name__ == "__main__":
    test_catalog_operations()
