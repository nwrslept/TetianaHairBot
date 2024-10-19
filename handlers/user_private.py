import os
from aiogram import  F, types, Router, Bot
from aiogram.filters import CommandStart, Command, or_f

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import clear_cart, get_cart, orm_get_actions, user_db  


from database.orm_query import check_isbusy, orm_add_schedule, orm_get_product, orm_get_products, orm_get_schedule, orm_update_schedule, add_to_cart, get_cart, remove_from_cart
from sqlalchemy.ext.asyncio import AsyncSession
import kbds.user_markups as nav

from kbds.inline import get_callback_btns
from database.orm_query import Database

from translations import _

user_private_router = Router()
db = Database('my_base.db')

class OrderInfo(StatesGroup):
    full_name = State()
    address = State()
    phone_number = State()


class Add(StatesGroup):
    id_product = State()
    full_name = State()
    index_adress = State()
    number_phon = State()

    product_for_change = None

admin_ids = os.getenv("ADMIN_ID").split(",")
admin_ids = [int(admin_id) for admin_id in admin_ids]


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    if not db.user_exists(message.from_user.id):
        await message.answer("Виберіть мову:\nVyberte jazyk:", reply_markup=nav.langMenu)
    else:
        lang = db.get_lang(message.from_user.id)
        await message.answer(_("Ласкаво просимо!", lang), reply_markup=nav.start_kb(lang))
        
@user_private_router.callback_query(F.data.startswith('lang_'))
async def setLanguage(callback: types.callback_query):
    if len(callback.data) > 5:
        lang = callback.data[5:]
        if not db.user_exists(callback.from_user.id):
            lang = callback.data[5:]
            db.add_user(callback.from_user.id, lang)
            await callback.message.answer(_("Успішна реєстрація!", lang), reply_markup=nav.start_kb(lang))
        else:
            # Якщо користувач вже існує, просто оновлюємо його мову
            db.update_lang(callback.from_user.id, lang)  # Оновлюємо мову
            await callback.message.answer(_("Мову успішно змінено!", lang), reply_markup=nav.start_kb(lang))
    else:
        # Обробляємо некоректні дані, наприклад, якщо `callback.data` містить некоректний формат
        await callback.message.answer(_("Невірний формат вибору мови.", lang))


@user_private_router.message(Command('id'))
async def cmd_id(message: types.Message):
    await message.edit_text(f'{message.from_user.id}')

@user_private_router.message(or_f(F.text.lower () == "найчастіші запитання❓", F.text.lower () == 'nejčastější dotazy❓'))
async def info(message: types.Message):
    lang = db.get_lang(message.from_user.id)
    await message.answer(_("Найчастіші запитання:",lang))
    await message.answer_photo("AgACAgIAAxkBAAIKqGbxqjyD2CbbWjlkekxraYUZktcVAAL55jEbCtWRS3D4js_QxFIoAQADAgADeQADNgQ")
    await message.answer(_('Опис процедур:',lang), reply_markup=nav.info_kb(lang))

@user_private_router.callback_query(F.data.startswith('_botox'))
async def botox(callback: types.callback_query):
    lang = db.get_lang(callback.from_user.id)
    await callback.message.edit_text(_('Ботокс - це...',lang),reply_markup=nav.back_kb(lang))

@user_private_router.callback_query(F.data.startswith('_keratin'))
async def keratin(callback: types.callback_query):
    lang = db.get_lang(callback.from_user.id)
    await callback.message.edit_text(_('Кератин - це...', lang),reply_markup=nav.back_kb(lang))

@user_private_router.callback_query(F.data.startswith('_collagen'))
async def collagen(callback: types.callback_query):
    lang = db.get_lang(callback.from_user.id)
    await callback.message.edit_text(_('Коллаген - це...', lang),reply_markup=nav.back_kb(lang))

@user_private_router.callback_query(F.data.startswith('_coldreg'))
async def coldreg(callback: types.callback_query):
    lang = db.get_lang(callback.from_user.id)
    await callback.message.edit_text(_('Холодне відновлення - це...',lang),reply_markup=nav.back_kb(lang))

@user_private_router.callback_query(F.data.startswith('_back'))
async def infoback(callback: types.callback_query):
    lang = db.get_lang(callback.from_user.id)
    await callback.message.edit_text(_('Виберіть процедуру:',lang), reply_markup=nav.info_kb(lang))




@user_private_router.message(F.text == ("Акції🎁"))
async def starring_at_actions(message: types.Message, session: AsyncSession):
    for action in await orm_get_actions(session):
        await message.answer(action.description)

@user_private_router.message(F.text == ("Akce🎁"))
async def starring_at_actionscz(message: types.Message, session: AsyncSession):
    for action in await orm_get_actions(session):
        await message.answer(action.description)
    

@user_private_router.message(or_f(F.text.lower() == "змінити мову🇺🇦/🇨🇿", F.text.lower() == 'změňte jazyk🇺🇦/🇨🇿'))
async def menu_cmd(message: types.Message):
    await message.answer("Виберіть мову\nVyber jazyk:", reply_markup=nav.langMenu)

@user_private_router.message((F.text.lower() == "записатись на прийом📅"))
async def schedule(message: types.Message, session: AsyncSession):
    schedules = await check_isbusy(session)
    if schedules:  # Якщо є доступні дати
        for schedule in schedules:
            await message.answer(f'Доступна дата:\n{schedule.date}📅\n{schedule.time}🕒',
                                 reply_markup=get_callback_btns(btns={
                                      'записатись': f'signup_{schedule.id}'
                                 }))
    await message.answer('А також можна замовити майстра до собе додому: @Tetiana_Senkiv')

@user_private_router.message((F.text.lower() == "domluvit si schůzku📅"))
async def schedule1(message: types.Message, session: AsyncSession):
    schedules = await check_isbusy(session)
    if schedules:  # Якщо є доступні дати
        for schedule in schedules:       
            await message.answer(f'Dostupné datum: \n{schedule.date}📅\n{schedule.time}🕒',
                                 reply_markup=get_callback_btns(btns={
                                      'přihlásit se': f'signup1_{schedule.id}'
                                 }))
    await message.answer('A mistra si můžete objednat i domů: @Tetiana_Senkiv')


@user_private_router.message(or_f(F.text == 'Список послуг📰', F.text == 'Seznam služeb📰'))
async def aboutus(message: types.Message):
    media = [
        InputMediaPhoto(media="AgACAgIAAxkBAAIKqGbxqjyD2CbbWjlkekxraYUZktcVAAL55jEbCtWRS3D4js_QxFIoAQADAgADeQADNgQ"),
        InputMediaPhoto(media="AgACAgIAAxkBAAIKqmbxqj99JQXBuv8L4GVX2svTNwxcAAL65jEbCtWRS-Af5JJ5QpYYAQADAgADeQADNgQ"),
        InputMediaPhoto(media="AgACAgIAAxkBAAIKrGbxqkI9RUXcgXWSIjrXqXDrTjMYAAL75jEbCtWRS3YYBv5x6iWuAQADAgADeQADNgQ"),
        InputMediaPhoto(media="AgACAgIAAxkBAAIKpmbxqjBukuSmpCIXdA0U5XDu6q-6AAL45jEbCtWRSxHq9ahIuqL3AQADAgADeQADNgQ"),
    ]
    await message.answer_media_group(media=media)

# @user_private_router.message(F.photo)
# async def photo(message: types.Message):
#     photo_data = message.photo[-1]
#     await message.answer(f"{photo_data}")

@user_private_router.message(or_f(F.text == 'Зворотній звязок☎️', F.text == 'Zpětná vazba☎️'))
async def feedback(message: types.Message):
    await message.answer('Telegram: @Tetiana_Senkiv\nPhone:+420792711477/+380685187690\nInstagram:https://www.instagram.com/tetiana_hair_beauty?igsh=MWV3eWdoMjlyejk4dw==')


@user_private_router.message(or_f(F.text == "Відгуки⭐", F.text == 'Recenze⭐'))
async def reviews(message: types.Message):
    lang = db.get_lang(message.from_user.id)
    media = [
        InputMediaPhoto(media=_("AgACAgIAAxkBAAIKqGbxqjyD2CbbWjlkekxraYUZktcVAAL55jEbCtWRS3D4js_QxFIoAQADAgADeQADNgQ", lang)),
    ]
    await message.answer_media_group(media=media)






@user_private_router.message(or_f(F.text.lower() == "замовити професійний догляд🛒", F.text.lower() == 'objednejte si odbornou péči🛒'))
async def buy(message: types.Message, session: AsyncSession, state: FSMContext):
    lang = db.get_lang(message.from_user.id)
    products = await orm_get_products(session)
    
    # Зберегти всі продукти в стан
    await state.update_data(products=[product.id for product in products], current_index=0)

    # Показати перший продукт
    if products:
        reply_message = await show_product(message, products[0], lang, 0)
        await state.update_data(reply_message_id=reply_message.message_id)

async def show_product(message: types.Message, product, lang, index):
    
    if lang == 'ua':
        reply_message = await message.answer_photo(
        product.image,
        caption=f"{product.name}\n{product.description}\n{round(product.price, 2)}kč",
        reply_markup=get_callback_btns(
            btns={
                _("⬅️", lang): f"prev_{index}",
                _("➡️", lang): f"next_{index}",
                _("Додати до корзини", lang): f"add_to_cart_{product.id}",
                _("Корзина🛒", lang): "viewcart_",
                
            }
        ),
    )
    else:
        reply_message = await message.answer_photo(
        product.image,
        caption=f"{product.namecz}\n{product.descriptioncz}\n{round(product.price, 2)}kč",
        reply_markup=get_callback_btns(
            btns={
                _("⬅️", lang): f"prev_{index}",
                _("➡️", lang): f"next_{index}",
                _("Додати до корзини", lang): f"add_to_cart_{product.id}",
                _("Корзина🛒", lang): "viewcart_",
                
            }
        ),
    )

    return reply_message  # Повертаємо надіслане повідомлення

@user_private_router.callback_query(F.data.startswith('prev_'))
async def show_previous(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    lang = db.get_lang(callback.from_user.id)
    data = await state.get_data()
    current_index = data.get('current_index', 0)
    products = data.get('products', [])

    if current_index > 0:
        current_index -= 1
        await state.update_data(current_index=current_index)
        await update_product_message(callback.message, products[current_index], lang, current_index, session)

@user_private_router.callback_query(F.data.startswith('next_'))
async def show_next(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    lang = db.get_lang(callback.from_user.id)
    data = await state.get_data()
    current_index = data.get('current_index', 0)
    products = data.get('products', [])

    if current_index < len(products) - 1:
        current_index += 1
        await state.update_data(current_index=current_index)
        await update_product_message(callback.message, products[current_index], lang, current_index, session)

async def update_product_message(message: types.Message, product_id: int, lang, index: int, session: AsyncSession):
    # Отримуємо продукт з бази даних за ID
    product = await orm_get_product(session, product_id)
    
    if product:
        if lang == 'ua': # Перевіряємо, чи продукт існує
            await message.edit_media(
                types.InputMediaPhoto(
                    media=product.image,  # Замість product.image використовуйте media
                    caption=f"{product.name}\n{product.description}\n{round(product.price, 2)}kč"
                ),
                reply_markup=get_callback_btns(
                    btns={
                        _("⬅️", lang): f"prev_{index}",
                        _("➡️", lang): f"next_{index}",
                        _("Додати до корзини", lang): f"add_to_cart_{product.id}",
                        _("Корзина🛒", lang): "viewcart_",
                    }
                )
            )
        else:
            await message.edit_media(
            types.InputMediaPhoto(
                media=product.image,  # Замість product.image використовуйте media
                caption=f"{product.namecz}\n{product.descriptioncz}\n{round(product.price, 2)}kč"
            ),
            reply_markup=get_callback_btns(
                btns={
                    _("⬅️", lang): f"prev_{index}",
                    _("➡️", lang): f"next_{index}",
                    _("Додати до корзини", lang): f"add_to_cart_{product.id}",
                    _("Корзина🛒", lang): "viewcart_",
                }
            )
        )







@user_private_router.callback_query(F.data.startswith('remove_from_cart_'))
async def remove_from_cart1(callback: types.CallbackQuery, session: AsyncSession):
    lang = db.get_lang(callback.from_user.id)
    user_id = callback.from_user.id
    product_id = int(callback.data.split('_')[-1])
    
    # Видалити товар з кошика
    await remove_from_cart(user_id, product_id, session)
    await callback.message.answer(_("Товар видалено з корзини", lang))


@user_private_router.callback_query(F.data.startswith('add_to_cart_'))
async def add_to_cart1(callback: types.CallbackQuery, session: AsyncSession):
    lang = db.get_lang(callback.from_user.id)
    user_id = callback.from_user.id
    product_id = int(callback.data.split('_')[-1])
    
    # Додати товар до корзини через базу даних
    await add_to_cart(user_id, product_id, 1, session)
    await callback.message.answer(_("Товар додано до корзини!", lang))

@user_private_router.callback_query(F.data.startswith('viewcart_'))
async def view_cart(callback: types.CallbackQuery, session: AsyncSession):
    lang = db.get_lang(callback.from_user.id)
    user_id = callback.from_user.id
    
    # Отримати вміст кошика з бази даних
    cart_items = await get_cart(user_id, session)
    
    if not cart_items:
        await callback.message.answer(_("Ваша корзина порожня", lang))
    else:
        for item in cart_items:
            product = item.product  # Отримуємо деталі товару через відношення
            await callback.message.answer_photo(
                product.image,
                caption=f"{product.name}\n{product.description}\n{round(product.price, 2)}kč",
                reply_markup=get_callback_btns(
                    btns={_("Видалити з корзини", lang): f"remove_from_cart_{product.id}"}
                ),
            )
        await callback.message.answer(_("Ваша корзина:",lang),
        reply_markup=get_callback_btns(
                btns={
                    _("Оформити замовлення", lang): f"order_{product.id}",
                }
            ))
        




@user_private_router.callback_query(F.data.startswith('signup_'))
async def delete_schedule(callback: types.callback_query, session: AsyncSession, bot: Bot):
    user = callback.from_user.username
    schedule_id= callback.data.split("_")[-1]
    schedule_for_change = await orm_get_schedule(session, int(schedule_id))
    await callback.message.answer(f"Ви успішно записались на {schedule_for_change.date}, о {schedule_for_change.time}\
                                  \nЧекаємо вас за адресою: Hlavni 1215,\
                                  \nЗа додатковою інформацією: @Tetiana_Senkiv", 
                                  reply_markup=get_callback_btns(btns={
                                     'Отримати геолокацію': f'send_location',
                                    'Відмінити запис': f'cancel_{schedule_id}',
                                 }))
    await orm_update_schedule(session, int(schedule_id), {
        "date": schedule_for_change.date,
        "time": schedule_for_change.time,
        "isbusy": True  # Змінюємо isbusy на True
    })
    for admin_id in admin_ids:
        await bot.send_message(admin_id, f"Користувач @{user} записався на {schedule_for_change.date}, о {schedule_for_change.time}")
    #await orm_delete_schedule(session, int(schedule_id))

@user_private_router.callback_query(F.data.startswith('signup1_'))
async def delete_schedule1(callback: types.callback_query, session: AsyncSession, bot: Bot):
    user = callback.from_user.username
    schedule_id= callback.data.split("_")[-1]
    schedule_for_change = await orm_get_schedule(session, int(schedule_id))
    await callback.message.answer(f"Úspěšně jste se zaregistrovali do {schedule_for_change.date}, {schedule_for_change.time}\
                                  \nČekáme na vás na Hlavní 1215,\
                                  \nDalší informace: @Tetiana_Senkiv", 
                                  reply_markup=get_callback_btns(btns={
                                     'Získejte geolokaci': f'send_location',
                                    'Zrušit zadání': f'cancel1_{schedule_id}',
                                 }))
    await orm_update_schedule(session, int(schedule_id), {
        "date": schedule_for_change.date,
        "time": schedule_for_change.time,
        "isbusy": True  # Змінюємо isbusy на True
    })
    for admin_id in admin_ids:
        await bot.send_message(admin_id, f"Користувач @{user} записався на {schedule_for_change.date}, о {schedule_for_change.time}")

@user_private_router.callback_query(F.data.startswith('send_location'))
async def send_location(callback: types.callback_query):
    lang = db.get_lang(callback.from_user.id)
    await callback.message.answer_location(49.20317636135491, 17.541798210167258)

@user_private_router.callback_query(F.data.startswith('cancel_'))
async def cancel_schedule(callback: types.callback_query, session: AsyncSession, bot: Bot):
    schedule_id = int(callback.data.split("_")[-1])
    schedule_for_change = await orm_get_schedule(session, schedule_id)
    await orm_update_schedule(session, schedule_id, {
        "date": schedule_for_change.date,
        "time": schedule_for_change.time,
        "isbusy": False  # Змінюємо isbusy на False
    })
    await callback.message.answer(f"Ви відмінили запис на {schedule_for_change.date}, о {schedule_for_change.time}")
    await callback.answer("Ваш запис скасовано!", show_alert=True)
    user = callback.from_user.username
    for admin_id in admin_ids:
        await bot.send_message(admin_id, f"Користувач @{user} відмінив запис на {schedule_for_change.date}, о {schedule_for_change.time}")
    schedule_data = {
        'date': schedule_for_change.date,
        'time': schedule_for_change.time
    }
    await orm_add_schedule(session, schedule_data)

@user_private_router.callback_query(F.data.startswith('cancel1_'))
async def cancel1_schedule(callback: types.callback_query, session: AsyncSession, bot: Bot):
    schedule_id = int(callback.data.split("_")[-1])
    schedule_for_change = await orm_get_schedule(session, schedule_id)
    await orm_update_schedule(session, schedule_id, {
        "date": schedule_for_change.date,
        "time": schedule_for_change.time,
        "isbusy": False  # Змінюємо isbusy на False
    })
    await callback.message.answer(f"Nahrávání jste zrušili dne {schedule_for_change.date}, {schedule_for_change.time}")
    await callback.answer("Váš záznam byl zrušen!", show_alert=True)
    user = callback.from_user.username
    for admin_id in admin_ids:
        await bot.send_message(admin_id,f"Користувач @{user} відмінив запис на {schedule_for_change.date}, о {schedule_for_change.time}")
    schedule_data = {
        'date': schedule_for_change.date,
        'time': schedule_for_change.time
    }
    await orm_add_schedule(session, schedule_data)

#FSM

@user_private_router.callback_query(F.data.startswith('order_'))
async def process_order(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    data_parts = callback.data.split('_')
    lang = db.get_lang(callback.from_user.id)

    if len(data_parts) < 2 or not data_parts[1].isdigit():
        await callback.answer("Помилка: недійсний формат замовлення.", show_alert=True)
        return

    product_id = int(data_parts[1])
    
    # Зберігаємо ID продукту в стані
    await state.update_data(product_id=product_id)
    
    # Запитуємо користувача про його ФІО
    await callback.message.answer(_("Введіть ФІО. (повні)",lang))
    await state.set_state(OrderInfo.full_name)  # Встановлюємо стан для отримання ФІО



@user_private_router.message(OrderInfo.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    lang = db.get_lang(message.from_user.id)

    await state.update_data(full_name=full_name)  # Зберігаємо ФІО в стані
    
    await message.answer(_("Укажіть індекс і адресу доставки",lang))
    await state.set_state(OrderInfo.address)  # Встановлюємо стан для адреси

@user_private_router.message(OrderInfo.address)
async def process_address(message: types.Message, state: FSMContext):
    address = message.text
    lang = db.get_lang(message.from_user.id)

    await state.update_data(address=address)  # Зберігаємо адресу в стані
    
    await message.answer(_("Введіть номер телефону починаючи з: +380, або +420",lang))
    await state.set_state(OrderInfo.phone_number)  # Встановлюємо стан для номера телефону

@user_private_router.message(OrderInfo.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)  # Зберігаємо номер телефону в стані

    lang = db.get_lang(message.from_user.id)
    user_data = await state.get_data()  # Отримуємо всі дані
    full_name = user_data.get('full_name')
    address = user_data.get('address')

    # Отримуємо ім'я користувача
    username = message.from_user.username if message.from_user.username else "Немає імені користувача"
    
    cart_items = await get_cart(message.from_user.id, session)  # Отримуємо вміст кошика

    # Формуємо список назв продуктів
    product_names = []
    for item in cart_items:
        product = item.product  # Отримуємо деталі товару через відношення
        product_names.append(product.name)  # Додаємо назву продукту в список

    # Формуємо повідомлення
    products_message = "\n".join(product_names) if product_names else "Кошик порожній."
    order_summary = (f"Нове замовлення від користувача: @{username}\n"
                     f"ФІО: {full_name}\n"
                     f"Адреса: {address}\n"
                     f"Телефон: {phone_number}\n"
                     f"Продукти:\n{products_message}")

    # Надсилаємо інформацію адміну
    for admin_id in admin_ids:
        await bot.send_message(admin_id, order_summary)
    await message.answer(_("Заказ оформлено, за додатковою інформацією: @Tetiana_Senkiv",lang))
    # Очищаємо кошик
    await clear_cart(message.from_user.id, session)  # Використовуємо clear_cart, який в свою чергу використовує remove_from_cart

    # Завершення стану
    await state.clear()  # Завершуємо стан







