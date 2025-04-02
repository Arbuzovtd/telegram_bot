#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для запуска Telegram-бота в режиме разработки.
Создает файл .env с токеном бота, если он не существует.
"""

import os
import sys

def setup_env():
    """Настраивает файл .env для запуска бота."""
    if not os.path.exists(".env"):
        print("Файл .env не найден. Создаем новый файл...")
        
        token = input("Введите токен вашего Telegram-бота: ")
        admin_ids = input("Введите ID администраторов через запятую (необязательно): ")
        
        with open(".env", "w") as f:
            f.write(f"TOKEN={token}\n")
            if admin_ids:
                f.write(f"ADMIN_IDS={admin_ids}\n")
            f.write("DEBUG=True\n")
            f.write("DATABASE_URL=sqlite:///bot_database.db\n")
        
        print("Файл .env успешно создан.")
    else:
        print("Файл .env уже существует.")

def run_bot():
    """Запускает бота."""
    try:
        from main import main
        print("Запуск бота...")
        main()
    except ImportError as e:
        print(f"Ошибка импорта: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка запуска бота: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Проверяем наличие файла .env
    setup_env()
    
    # Запускаем бота
    run_bot()
