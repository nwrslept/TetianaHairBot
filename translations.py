translations = {
    'cz': {
        'Успішна реєстрація!': 'Úspěšná registrace!',
        'Ласкаво просимо!': 'Vítejte!',
        'Змінити мову🇺🇦/🇨🇿': 'Změňte jazyk🇺🇦/🇨🇿',
        'Доступні дати записів📅': 'Dostupné termíny nahrávání📅',
        'Про нас💬':'O nás💬',
        'Відгуки⭐': 'Recenze⭐',
        'Купити': 'Nakoupit',
        'Невірний формат вибору мови.': 'Formát výběru jazyka je nesprávný.',
        'Мову успішно змінено!': 'Jazyk úspěšně změněn!',
        'записатись': 'přihlásit se',
        'Замовити професійний догляд🛒:': 'Objednejte si odbornou péči🛒:',
        'Посилання на Google Maps надіслано!': 'Odkaz na Google Maps odeslán!',
        'Замовити професійний догляд🛒': 'Objednejte si odbornou péči🛒',
        'Замовити': 'Objednávka',
        'Введіть ФІО. (повні)': 'Zadejte své celé jméno.',
        'Укажіть індекс і адресу доставки': 'Zadejte PSČ a dodací adresu',
        'Допущена помилка❗': 'Došlo k chybě❗',
        'Введіть номер телефона починаючи з: +380, або +420': 'Zadejte telefonní číslo začínající na: +380 nebo +420',
        'Введення номера неправильне❗': 'Zadání čísla je nesprávné❗',
        'Заказ оформлено, за додатковою інформацією: @nwrslept': 'Objednávka je zadána, pro další informace: @nwrslept',
        '': '',
        '': '',
        '': '',
        '': '',
        '': '',
        '': '',
    }
}

def _(text, lang='ua'):
    if lang == 'ua':
        return text
    else:
        global translations
        try:
            return translations[lang][text]
        except:
            return text