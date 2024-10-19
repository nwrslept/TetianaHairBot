translations = {
    'cz': {
        'Успішна реєстрація!': 'Úspěšná registrace!',
        'Ласкаво просимо!': 'Vítejte!',
        'Змінити мову🇺🇦/🇨🇿': 'Změňte jazyk🇺🇦/🇨🇿',
        'Записатись на прийом📅': 'Domluvit si schůzku📅',
        'Список послуг📰':'Seznam služeb📰',
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
        'Введіть номер телефону починаючи з: +380, або +420': 'Zadejte telefonní číslo začínající na: +380 nebo +420',
        'Введення номера неправильне❗': 'Zadání čísla je nesprávné❗',
        'Заказ оформлено, за додатковою інформацією: @Tetiana_Senkiv': 'Objednávka je zadána, pro další informace: @Tetiana_Senkiv',
        'Зворотній звязок☎️': 'Zpětná vazba☎️',
        'А також можна замовити майстра до собе додому: @Tetiana_Senkiv': 'A mistra si můžete objednat i domů: @Tetiana_Senkiv',
        'Відмінити': 'Zrušit',
        'Оформлення замовлення відмінено!': 'Objednávka byla zrušena!',
        'Акції🎁': 'Akce🎁',
        'Найчастіші запитання❓': 'Nejčastější dotazy❓',
        'Ботокс - це...': 'Botox je...',
        'Кератин - це...': 'Collagen je...',
        'Коллаген - це...': 'Kolagen je...',
        'Холодне відновлення - це...': 'Regenerace za studena je...',
        'Виберіть процедуру:': 'Vyberte postup:',
        'Ботокс': 'Botox',
        'Кератин': 'Keratin',
        'Коллаген': 'Collagen',
        'Холодне відновлення': 'Regenerace za studena',
        'Назад': 'Zpatky',
        'Опис процедур:': 'Popis procedur:',
        'Найчастіші запитання:': 'Často kladené otázky:',
        'Додати до корзини': 'Přidat do košíku',
        'Корзина🛒': 'Košík 🛒',
        'Товар видалено з корзини': 'Produkt byl odstraněn z nákupního košíku',
        'Товар додано до корзини!': 'Produkt byl přidán do košíku!',
        'Ваша корзина порожня': 'Váš nákupní košík je prázdný',
        'Видалити з корзини': 'Odebrat z košíku',
        'Ваша корзина:': 'Váš nákupní košík:',
        'Оформити замовлення': 'Udělejte objednávku',
        '': '',
        '': '',
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