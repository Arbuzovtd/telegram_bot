from telegram import Update
from telegram.ext import ContextTypes
from ..database.db import Database
from ..utils.helpers import validate_product_code, format_order_message, format_photo_video_order_message, get_admin_ids

# Инициализация базы данных
db = Database()

async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Регистрирует пользователя в базе данных."""
    user = update.effective_user
    db.add_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )

async def save_order(update: Update, context: ContextTypes.DEFAULT_TYPE, has_photo=False):
    """Сохраняет заказ в базу данных."""
    user_id = update.effective_user.id
    product_code = context.user_data.get('product_code', '')
    description = context.user_data.get('order_description', '')
    photo_id = context.user_data.get('photo_id', None) if has_photo else None
    
    order_id = db.add_order(
        user_id=user_id,
        product_code=product_code,
        description=description,
        has_photo=has_photo,
        photo_id=photo_id
    )
    
    # Отправка уведомления администраторам
    if order_id:
        admin_ids = get_admin_ids()
        message = format_order_message(context.user_data, has_photo)
        
        for admin_id in admin_ids:
            try:
                if has_photo and photo_id:
                    await context.bot.send_photo(
                        chat_id=admin_id,
                        photo=photo_id,
                        caption=message
                    )
                else:
                    await context.bot.send_message(
                        chat_id=admin_id,
                        text=message
                    )
            except Exception as e:
                print(f"Error sending notification to admin {admin_id}: {e}")
    
    return order_id

async def save_photo_video_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохраняет заказ фото/видео в базу данных."""
    user_id = update.effective_user.id
    description = context.user_data.get('photo_video_order', '')
    
    order_id = db.add_photo_video_order(
        user_id=user_id,
        description=description
    )
    
    # Отправка уведомления администраторам
    if order_id:
        admin_ids = get_admin_ids()
        message = format_photo_video_order_message(context.user_data)
        
        for admin_id in admin_ids:
            try:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=message
                )
            except Exception as e:
                print(f"Error sending notification to admin {admin_id}: {e}")
    
    return order_id

async def get_user_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получает список заказов пользователя."""
    user_id = update.effective_user.id
    return db.get_user_orders(user_id)

async def get_user_photo_video_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получает список заказов фото/видео пользователя."""
    user_id = update.effective_user.id
    return db.get_user_photo_video_orders(user_id)
