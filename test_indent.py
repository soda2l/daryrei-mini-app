#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Тест для проверки отступов

with open('bot.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Найдем строку с start_command
for i, line in enumerate(lines):
    if 'def start_command' in line:
        print(f"Строка {i+1}: {repr(line)}")
        print(f"Отступ: {len(line) - len(line.lstrip())} символов")
        print(f"Предыдущая строка: {repr(lines[i-1])}")
        print(f"Следующая строка: {repr(lines[i+1])}")
        break
