class ReplyKeyboardMarkup:
    def __init__(self, keyboard=None, resize_keyboard=False):
        self.keyboard = keyboard
        self.resize_keyboard = resize_keyboard

class KeyboardButton:
    def __init__(self, text, request_contact=False):
        self.text = text
        self.request_contact = request_contact

class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard=None):
        self.inline_keyboard = inline_keyboard

class InlineKeyboardButton:
    def __init__(self, text, url=None):
        self.text = text
        self.url = url
