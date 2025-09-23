#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Тест для проверки структуры класса

with open('bot.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Найдем начало класса
class_start = None
for i, line in enumerate(lines):
    if line.strip().startswith('class DaryReiBot'):
        class_start = i
        print(f"Класс начинается на строке {i+1}")
        break

if class_start is not None:
    # Найдем все методы класса
    methods = []
    for i in range(class_start, len(lines)):
        line = lines[i]
        if line.strip().startswith('def ') or line.strip().startswith('async def '):
            if line.startswith('    '):  # Метод класса
                method_name = line.strip().split('(')[0].split()[-1]
                methods.append(f"Строка {i+1}: {method_name}")
    
    print("Методы класса:")
    for method in methods:
        print(f"  {method}")
    
    # Найдем конец класса
    for i in range(class_start, len(lines)):
        line = lines[i]
        if line.strip() and not line.startswith('    ') and not line.startswith('#'):
            if not line.strip().startswith('class '):
                print(f"Класс заканчивается на строке {i}")
                break
