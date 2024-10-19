from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from translations import _




admin_kb = ReplyKeyboardBuilder()
admin_kb.add (
    KeyboardButton(text='Добавити дату для запису'),
    KeyboardButton(text='Дати записів'),
    KeyboardButton(text='Добавити продукт'),
    KeyboardButton(text='Список продуктів'),
    KeyboardButton(text='Добавити замітку'),
    KeyboardButton(text='Переглянути замітки'),
    KeyboardButton(text='Добавити акцію'),
    KeyboardButton(text='Список акцій'),

)
admin_kb.adjust(2, 2, 2, 2)




del_kbd = ReplyKeyboardRemove()