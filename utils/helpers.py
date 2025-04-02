import os
import logging
from datetime import datetime

def setup_logger():
    """Настраивает и возвращает логгер для бота."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    return logging.getLogger(__name__)

def validate_product_code(code):
    """
    Проверяет корректность кода товара.
    В данной реализации считаем корректным код, состоящий только из цифр.
    """
    return code.isdigit()

def save_file_from_telegram(file, destination_folder):
    """
    Сохраняет файл, полученный от пользователя, в указанную папку.
    Возвращает путь к сохраненному файлу.
    """
    # Создаем папку, если она не существует
    os.makedirs(destination_folder, exist_ok=True)
    
    # Генерируем уникальное имя файла на основе текущего времени
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(file.file_path)[1]
    file_name = f"{timestamp}{file_extension}"
    file_path = os.path.join(destination_folder, file_name)
    
    # Сохраняем файл
    file.download(file_path)
    
    return file_path

def format_order_message(user_data, has_photo=False):
    """
    Форматирует сообщение о заказе для отправки администраторам.
    """
    product_code = user_data.get('product_code', 'Не указан')
    description = user_data.get('order_description', 'Не указано')
    
    message = f"Новый заказ!\n\n"
    message += f"Код товара: {product_code}\n"
    message += f"Описание: {description}\n"
    message += f"Фото: {'Да' if has_photo else 'Нет'}\n"
    message += f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
    
    return message

def format_photo_video_order_message(user_data):
    """
    Форматирует сообщение о заказе фото/видео для отправки администраторам.
    """
    description = user_data.get('photo_video_order', 'Не указано')
    
    message = f"Новый заказ фото/видео!\n\n"
    message += f"Описание: {description}\n"
    message += f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
    
    return message

def get_admin_ids():
    """
    Получает список ID администраторов из переменных окружения.
    """
    admin_ids_str = os.getenv("ADMIN_IDS", "")
    if not admin_ids_str:
        return []
    
    try:
        return [int(admin_id.strip()) for admin_id in admin_ids_str.split(",")]
    except ValueError:
        return []
