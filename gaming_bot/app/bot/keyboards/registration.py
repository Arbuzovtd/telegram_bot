from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

share_phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='📱 Поделиться номером', request_contact=True)]],
    resize_keyboard=True
)
