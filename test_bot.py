#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестовый скрипт для проверки работоспособности Telegram-бота.
Этот скрипт проверяет основные компоненты бота без запуска полного приложения.
"""

import os
import sys
import unittest
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Проверка наличия токена
TOKEN = os.getenv("TOKEN", "")

class BotTestCase(unittest.TestCase):
    """Тесты для проверки компонентов Telegram-бота."""
    
    def test_environment_setup(self):
        """Проверяет настройку окружения."""
        # Проверка наличия всех необходимых директорий
        self.assertTrue(os.path.exists("handlers"))
        self.assertTrue(os.path.exists("database"))
        self.assertTrue(os.path.exists("keyboards"))
        self.assertTrue(os.path.exists("utils"))
        
        # Проверка наличия всех необходимых файлов
        self.assertTrue(os.path.exists("main.py"))
        self.assertTrue(os.path.exists("handlers/__init__.py"))
        self.assertTrue(os.path.exists("database/__init__.py"))
        self.assertTrue(os.path.exists("keyboards/__init__.py"))
        self.assertTrue(os.path.exists("utils/__init__.py"))
    
    def test_database_module(self):
        """Проверяет модуль базы данных."""
        try:
            from database.db import Database
            
            # Создание тестовой базы данных
            test_db = Database("test_database.db")
            
            # Проверка создания таблиц
            self.assertIsNotNone(test_db)
            
            # Удаление тестовой базы данных
            if os.path.exists("test_database.db"):
                os.remove("test_database.db")
                
        except ImportError as e:
            self.fail(f"Не удалось импортировать модуль базы данных: {e}")
    
    def test_keyboards_module(self):
        """Проверяет модуль клавиатур."""
        try:
            from keyboards.keyboards import get_main_keyboard, get_back_keyboard
            
            # Проверка создания клавиатур
            main_keyboard = get_main_keyboard()
            back_keyboard = get_back_keyboard()
            
            self.assertIsNotNone(main_keyboard)
            self.assertIsNotNone(back_keyboard)
            
        except ImportError as e:
            self.fail(f"Не удалось импортировать модуль клавиатур: {e}")
    
    def test_utils_module(self):
        """Проверяет модуль утилит."""
        try:
            from utils.helpers import validate_product_code
            
            # Проверка функции валидации кода товара
            self.assertTrue(validate_product_code("12345"))
            self.assertFalse(validate_product_code("abc123"))
            
        except ImportError as e:
            self.fail(f"Не удалось импортировать модуль утилит: {e}")
    
    def test_token_availability(self):
        """Проверяет наличие токена бота."""
        # Этот тест будет пропущен, так как токен не установлен в тестовой среде
        if not TOKEN:
            self.skipTest("Токен бота не установлен в переменных окружения")
        else:
            self.assertTrue(len(TOKEN) > 0)

if __name__ == "__main__":
    # Изменение текущей директории на директорию с ботом
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Запуск тестов
    unittest.main()
