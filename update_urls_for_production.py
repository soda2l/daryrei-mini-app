#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

def update_urls_for_production():
    """Обновляет URL в index.html для продакшена"""
    
    # Читаем файл
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем localhost на продакшен URL
    replacements = [
        ('http://localhost:8000/api/catalog', 'https://daryreibot.duckdns.org/api/catalog'),
        ('http://localhost:8000/api/order', 'https://daryreibot.duckdns.org/api/order'),
        ('http://localhost:8000/images/', 'https://daryreibot.duckdns.org/images/'),
    ]
    
    for old_url, new_url in replacements:
        content = content.replace(old_url, new_url)
    
    # Сохраняем обновленный файл
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ URL обновлены для продакшена")
    print("📝 Изменения:")
    for old_url, new_url in replacements:
        print(f"   {old_url} → {new_url}")

def update_urls_for_development():
    """Возвращает URL обратно для локальной разработки"""
    
    # Читаем файл
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем продакшен URL на localhost
    replacements = [
        ('https://daryreibot.duckdns.org/api/catalog', 'http://localhost:8000/api/catalog'),
        ('https://daryreibot.duckdns.org/api/order', 'http://localhost:8000/api/order'),
        ('https://daryreibot.duckdns.org/images/', 'http://localhost:8000/images/'),
    ]
    
    for old_url, new_url in replacements:
        content = content.replace(old_url, new_url)
    
    # Сохраняем обновленный файл
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ URL обновлены для локальной разработки")
    print("📝 Изменения:")
    for old_url, new_url in replacements:
        print(f"   {old_url} → {new_url}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        update_urls_for_development()
    else:
        update_urls_for_production()
