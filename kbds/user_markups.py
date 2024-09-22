from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from translations import _
from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_kb(lang):
    btnLang = KeyboardButton(text=_('Змінити мову🇺🇦/🇨🇿', lang))
    btnSchedules = KeyboardButton(text=_('Доступні дати записів📅', lang))
    btnAbout = KeyboardButton(text=_('Про нас💬', lang))
    btnReviews = KeyboardButton(text=_('Відгуки⭐', lang))
    btnBuy = KeyboardButton(text=_('Замовити професійний догляд🛒', lang))
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [btnLang, btnSchedules],
            [btnAbout],
            [btnReviews, btnBuy]
        ],
        resize_keyboard=True
    )
    return keyboard




langUA = InlineKeyboardButton(text='Українська🇺🇦', callback_data='lang_ua')
langCZ = InlineKeyboardButton(text='Čeština🇨🇿', callback_data='lang_cz')

langMenu = InlineKeyboardMarkup(inline_keyboard=[
    [langUA, langCZ]
])

