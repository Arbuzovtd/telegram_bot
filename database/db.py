import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_file="bot_database.db"):
        """Инициализация базы данных."""
        self.db_file = db_file
        self.conn = None
        self.create_tables()
    
    def connect(self):
        """Подключение к базе данных."""
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def create_tables(self):
        """Создание необходимых таблиц в базе данных."""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            registration_date TIMESTAMP
        )
        ''')
        
        # Таблица заказов
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            product_code TEXT,
            description TEXT,
            has_photo BOOLEAN,
            photo_id TEXT,
            order_date TIMESTAMP,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users (telegram_id)
        )
        ''')
        
        # Таблица заказов фото/видео
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS photo_video_orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            description TEXT,
            order_date TIMESTAMP,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users (telegram_id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, telegram_id, username, first_name, last_name):
        """Добавление нового пользователя в базу данных."""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO users (telegram_id, username, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?)",
                (telegram_id, username, first_name, last_name, datetime.now())
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
        finally:
            conn.close()
    
    def add_order(self, user_id, product_code, description, has_photo=False, photo_id=None):
        """Добавление нового заказа в базу данных."""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO orders (user_id, product_code, description, has_photo, photo_id, order_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_id, product_code, description, has_photo, photo_id, datetime.now(), "new")
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding order: {e}")
            return None
        finally:
            conn.close()
    
    def add_photo_video_order(self, user_id, description):
        """Добавление нового заказа фото/видео в базу данных."""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO photo_video_orders (user_id, description, order_date, status) VALUES (?, ?, ?, ?)",
                (user_id, description, datetime.now(), "new")
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding photo/video order: {e}")
            return None
        finally:
            conn.close()
    
    def get_user_orders(self, user_id):
        """Получение всех заказов пользователя."""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM orders WHERE user_id = ? ORDER BY order_date DESC",
                (user_id,)
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting user orders: {e}")
            return []
        finally:
            conn.close()
    
    def get_user_photo_video_orders(self, user_id):
        """Получение всех заказов фото/видео пользователя."""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM photo_video_orders WHERE user_id = ? ORDER BY order_date DESC",
                (user_id,)
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting user photo/video orders: {e}")
            return []
        finally:
            conn.close()
    
    def update_order_status(self, order_id, status):
        """Обновление статуса заказа."""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "UPDATE orders SET status = ? WHERE id = ?",
                (status, order_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating order status: {e}")
            return False
        finally:
            conn.close()
    
    def update_photo_video_order_status(self, order_id, status):
        """Обновление статуса заказа фото/видео."""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "UPDATE photo_video_orders SET status = ? WHERE id = ?",
                (status, order_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating photo/video order status: {e}")
            return False
        finally:
            conn.close()
