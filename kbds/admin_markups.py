from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from translations import _




admin_kb = ReplyKeyboardBuilder()
admin_kb.add (
    KeyboardButton(text='Добавити дату для запису'),
    KeyboardButton(text='Дати записів'),
    KeyboardButton(text='Добавити продукт'),
    KeyboardButton(text='Список продуктів'),
    KeyboardButton(text='Добавити відгук'),
    KeyboardButton(text='Список відгуків'),
    KeyboardButton(text='Добавити замітку'),
    KeyboardButton(text='Переглянути замітки'),
)
admin_kb.adjust(2, 2, 2, 2)




del_kbd = ReplyKeyboardRemove()