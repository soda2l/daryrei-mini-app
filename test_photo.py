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

def test_photo_processing():
    """Тест обработки фото"""
    print("Тестируем обработку фото...")
    
    # Проверяем папку images
    images_dir = "images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print(f"✅ Создана папка: {images_dir}")
    else:
        print(f"✅ Папка существует: {images_dir}")
    
    # Проверяем права на запись
    test_file = os.path.join(images_dir, "test.txt")
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("✅ Права на запись в папку images есть")
    except Exception as e:
        print(f"❌ Нет прав на запись в папку images: {e}")
        return
    
    # Проверяем каталог
    try:
        with open("catalog.json", 'r', encoding='utf-8') as f:
            catalog = json.load(f)
        print("✅ Каталог загружен")
    except Exception as e:
        print(f"❌ Ошибка загрузки каталога: {e}")
        return
    
    # Проверяем товары
    products = catalog.get("products", [])
    if not products:
        print("❌ В каталоге нет товаров")
        return
    
    print(f"✅ Найдено товаров: {len(products)}")
    
    # Показываем первый товар
    first_product = products[0]
    print(f"Первый товар: {first_product.get('name', 'Без названия')}")
    print(f"ID: {first_product.get('id', 'Нет ID')}")
    print(f"Фото: {first_product.get('images', [])}")
    
    print("\n✅ Тест завершен успешно!")

if __name__ == "__main__":
    test_photo_processing()
