from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from translations import _

def start_kb(lang):
    btnLang = KeyboardButton(text=_('Змінити мову🇺🇦/🇨🇿', lang))
    btnSchedules = KeyboardButton(text=_('Записатись на прийом📅', lang))
    btnAbout = KeyboardButton(text=_('Список послуг📰', lang))
    btnReviews = KeyboardButton(text=_('Відгуки⭐', lang))
    btnBuy = KeyboardButton(text=_('Замовити професійний догляд🛒', lang))
    btnFeedback = KeyboardButton(text=_('Зворотній звязок☎️', lang))
    btnAction = KeyboardButton(text=_('Акції🎁', lang))
    btnInfo = KeyboardButton(text=_('Найчастіші запитання❓', lang))


    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [btnLang, btnSchedules],
            [btnBuy, btnInfo],
            [btnAbout, btnReviews, btnAction],
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

def info_kb(lang):
    botox = InlineKeyboardButton(text=_('Ботокс',lang), callback_data='_botox')
    keratin = InlineKeyboardButton(text=_('Кератин',lang), callback_data='_keratin')
    collagen = InlineKeyboardButton(text=_('Коллаген',lang), callback_data='_collagen')
    coldregeneration = InlineKeyboardButton(text=_('Холодне відновлення',lang), callback_data='_coldreg')

    InfoMenu = InlineKeyboardMarkup(inline_keyboard=[
        [botox],
        [keratin],
        [collagen],
        [coldregeneration],
    ])
    return InfoMenu


def back_kb(lang):
    back = InlineKeyboardButton(text=_('Назад', lang), callback_data='_back')

    backMenu = InlineKeyboardMarkup(inline_keyboard=[
        [back]
    ])
    return backMenu