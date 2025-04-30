from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Telefon raqam yuborish📲", request_contact=True)]], resize_keyboard=True
)

code = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Code yuborish📨")]], resize_keyboard=True
)