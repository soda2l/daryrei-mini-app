#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import os
import time

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Путь к файлу каталога
CATALOG_FILE = "catalog.json"

def init_catalog():
    """Инициализация каталога"""
    try:
        if os.path.exists(CATALOG_FILE):
            with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
                catalog = json.load(f)
            logger.info("Каталог загружен из файла")
            return catalog
        else:
            # Создаем базовый каталог
            catalog = {
                "categories": [],
                "products": []
            }
            with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
                json.dump(catalog, f, ensure_ascii=False, indent=2)
            logger.info("Создан новый каталог")
            return catalog
    except Exception as e:
        logger.error(f"Ошибка при инициализации каталога: {e}")
        return {"categories": [], "products": []}

def test_catalog():
    """Тест каталога"""
    print("Тестируем каталог...")
    
    catalog = init_catalog()
    
    print(f"Категорий: {len(catalog.get('categories', []))}")
    print(f"Товаров: {len(catalog.get('products', []))}")
    
    # Показываем первые 3 товара
    products = catalog.get('products', [])
    for i, product in enumerate(products[:3], 1):
        print(f"{i}. {product.get('name', 'Без названия')} - {product.get('price', 0)} ₽")
    
    print("Тест завершен!")

if __name__ == "__main__":
    test_catalog()
