from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from translations import _
from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_kb(lang):
    btnLang = KeyboardButton(text=_('Змінити мову🇺🇦/🇨🇿', lang))
    btnSchedules = KeyboardButton(text=_('Доступні дати записів📅', lang))
    btnAbout = KeyboardButton(text=_('Список послуг📰', lang))
    btnReviews = KeyboardButton(text=_('Відгуки⭐', lang))
    btnBuy = KeyboardButton(text=_('Замовити професійний догляд🛒', lang))
    btnFeedback = KeyboardButton(text=_('Зворотній звязок☎️', lang))
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [btnLang, btnSchedules],
            [btnBuy],
            [btnAbout, btnReviews],
            [btnFeedback],
        ],
        resize_keyboard=True
    )
    return keyboard




langUA = InlineKeyboardButton(text='Українська🇺🇦', callback_data='lang_ua')
langCZ = InlineKeyboardButton(text='Čeština🇨🇿', callback_data='lang_cz')

langMenu = InlineKeyboardMarkup(inline_keyboard=[
    [langUA, langCZ]
])

