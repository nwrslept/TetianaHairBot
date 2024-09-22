import os
from aiogram import  F, types, Router
from aiogram.filters import CommandStart, Command, or_f

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Schedule
from database.orm_query import user_db  


from database.orm_query import check_isbusy, orm_add_schedule, orm_delete_schedule, orm_get_product, orm_get_products, orm_get_reviews, orm_get_schedule, orm_get_schedules, orm_update_schedule
from sqlalchemy.ext.asyncio import AsyncSession
import kbds.user_markups as nav

from kbds.inline import get_callback_btns
from database.orm_query import Database

from translations import _

user_private_router = Router()
db = Database('my_base.db')



class Add(StatesGroup):
    id_product = State()
    full_name = State()
    index_adress = State()
    number_phon = State()


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
    await message.answer(f'{message.from_user.id}')

    

@user_private_router.message(or_f(F.text.lower() == "змінити мову🇺🇦/🇨🇿", F.text.lower() == 'změňte jazyk🇺🇦/🇨🇿'))
async def menu_cmd(message: types.Message):
    await message.answer("Виберіть мову\nVyber jazyk:", reply_markup=nav.langMenu)

@user_private_router.message((F.text.lower() == "доступні дати записів📅"))
async def schedule(message: types.Message, session: AsyncSession):
    schedules = await check_isbusy(session)
    if schedules:  # Якщо є доступні дати
        for schedule in schedules:
            await message.answer(f'Доступна дата:\n{schedule.date}📅\n{schedule.time}🕒',
                                 reply_markup=get_callback_btns(btns={
                                      'записатись': f'signup_{schedule.id}'
                                 }))

@user_private_router.message((F.text.lower() == "dostupné termíny nahrávání📅"))
async def schedule1(message: types.Message, session: AsyncSession):
    schedules = await check_isbusy(session)
    if schedules:  # Якщо є доступні дати
        for schedule in schedules:       
            await message.answer(f'Dostupné datum: \n{schedule.date}📅\n{schedule.time}🕒',
                                 reply_markup=get_callback_btns(btns={
                                      'přihlásit se': f'signup1_{schedule.id}'
                                 }))


@user_private_router.message(F.text == 'Про нас💬')
async def aboutus(message: types.Message):
    lang = db.get_lang(message.from_user.id)
    await message.answer('Ляллялялял')




@user_private_router.message(F.text == "Відгуки⭐")
async def starring_at_review(message: types.Message, session: AsyncSession):
    for review in await orm_get_reviews(session):
        await message.answer_photo(
            review.image,
            caption=review.description
        )
            
        

@user_private_router.message(F.text.lower() == 'objednejte si odbornou péči🛒')
async def buycz(message: types.Message, session: AsyncSession):
    lang = db.get_lang(message.from_user.id)
    await message.answer(_("Замовити професійний догляд🛒:", lang))
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"{product.name}\
                    \n{product.description}\nCena: {round(product.price, 2)}kč",
            reply_markup=get_callback_btns(
                btns={
                    _("Замовити",lang): f"order_{product.id}",
                }
            ),
        )

@user_private_router.message(F.text.lower() == "замовити професійний догляд🛒")
async def buy(message: types.Message, session: AsyncSession):
    lang = db.get_lang(message.from_user.id)
    await message.answer(_("Замовити професійний догляд🛒:", lang))
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"{product.name}\
                    \n{product.description}\nЦіна: {round(product.price, 2)}kč",
            reply_markup=get_callback_btns(
                btns={
                    _("Замовити",lang): f"order_{product.id}",
                }
            ),
        )


    


@user_private_router.callback_query(F.data.startswith('signup_'))
async def delete_schedule(callback: types.callback_query, session: AsyncSession):
    user = callback.from_user.username
    schedule_id= callback.data.split("_")[-1]
    schedule_for_change = await orm_get_schedule(session, int(schedule_id))
    await callback.message.answer(f"Ви успішно записались на {schedule_for_change.date}, о {schedule_for_change.time}\
                                  \nЧекаємо вас за адресою: Hlavni 1215,\
                                  \nЗа додатковою інформацією: @nwrslept", 
                                  reply_markup=get_callback_btns(btns={
                                     'Отримати геолокацію': f'send_location',
                                    'Відмінити запис': f'cancel_{schedule_id}',
                                 }))
    await orm_update_schedule(session, int(schedule_id), {
        "date": schedule_for_change.date,
        "time": schedule_for_change.time,
        "isbusy": True  # Змінюємо isbusy на True
    })


    input_schedule = int(os.getenv("ADMIN_ID"))
    if callback.from_user.id == input_schedule:
        await callback.message.answer(f"Користувач @{user} записався на {schedule_for_change.date}, о {schedule_for_change.time}")
    #await orm_delete_schedule(session, int(schedule_id))

@user_private_router.callback_query(F.data.startswith('signup1_'))
async def delete_schedule1(callback: types.callback_query, session: AsyncSession):
    user = callback.from_user.username
    schedule_id= callback.data.split("_")[-1]
    schedule_for_change = await orm_get_schedule(session, int(schedule_id))
    await callback.message.answer(f"Úspěšně jste se zaregistrovali do {schedule_for_change.date}, {schedule_for_change.time}\
                                  \nČekáme na vás na Hlavní 1215,\
                                  \nDalší informace: @nwrslept", 
                                  reply_markup=get_callback_btns(btns={
                                     'Získejte geolokaci': f'send_location',
                                    'Zrušit zadání': f'cancel1_{schedule_id}',
                                 }))
    await orm_update_schedule(session, int(schedule_id), {
        "date": schedule_for_change.date,
        "time": schedule_for_change.time,
        "isbusy": True  # Змінюємо isbusy на True
    })
    input_schedule = int(os.getenv("ADMIN_ID"))
    if callback.from_user.id == input_schedule:
        await callback.message.answer(f"Користувач @{user} записався на {schedule_for_change.date}, о {schedule_for_change.time}")



@user_private_router.callback_query(F.data.startswith('send_location'))
async def send_location(callback: types.callback_query):
    lang = db.get_lang(callback.from_user.id)
    await callback.message.answer("https://www.google.com/maps/search/?api=1&query=49.20317636135491,17.541798210167258")
    await callback.answer(_("Посилання на Google Maps надіслано!", lang))

@user_private_router.callback_query(F.data.startswith('cancel_'))
async def cancel_schedule(callback: types.callback_query, session: AsyncSession):
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
    input_schedule = int(os.getenv("ADMIN_ID"))
    if callback.from_user.id == input_schedule:
        await callback.message.answer(f"Користувач @{user} відмінив запис на {schedule_for_change.date}, о {schedule_for_change.time}")
    schedule_data = {
        'date': schedule_for_change.date,
        'time': schedule_for_change.time
    }
    await orm_add_schedule(session, schedule_data)

@user_private_router.callback_query(F.data.startswith('cancel1_'))
async def cancel1_schedule(callback: types.callback_query, session: AsyncSession):
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
    input_schedule = int(os.getenv("ADMIN_ID"))
    if callback.from_user.id == input_schedule:
        await callback.message.answer(f"Користувач @{user} відмінив запис на {schedule_for_change.date}, о {schedule_for_change.time}")
    schedule_data = {
        'date': schedule_for_change.date,
        'time': schedule_for_change.time
    }
    await orm_add_schedule(session, schedule_data)






#FSM order

@user_private_router.callback_query(F.data.startswith('order_'))
async def user_order(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
        lang = db.get_lang(callback.from_user.id)
        product_id= callback.data.split("_")[-1]
        await state.update_data(id_product=product_id)
        await callback.message.answer(text=_("Введіть ФІО. (повні)", lang), reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(Add.full_name)



@user_private_router.message(Add.full_name, F.text)
async def addAdress(message: Message, state: FSMContext):
    lang = db.get_lang(message.from_user.id)
    name = message.text.replace(" ", "")    
    if name.isalpha() == True:
        await state.update_data(full_name=message.text.title())

        await message.answer(text=_("Укажіть індекс і адресу доставки", lang))
        await state.set_state(Add.index_adress)
    else:
        await message.answer(text=_("Допущена помилка❗", lang))


@user_private_router.message(Add.index_adress, F.text)
async def addPhon(message: Message, state: FSMContext):
    lang = db.get_lang(message.from_user.id)
    await state.update_data(index_adress=message.text)

    await message.answer(text=_("Введіть номер телефона починаючи з: +380, або +420",lang))
    await state.set_state(Add.number_phon)


@user_private_router.message(Add.number_phon, F.text)
async def add_input(message: Message, state: FSMContext, session: AsyncSession):
    lang = db.get_lang(message.from_user.id)
    user = message.from_user.username


    num_phon = message.text.replace("+", "")
    if num_phon.isnumeric() == False:   
        await message.answer(_("Введення номера неправильне❗",lang))
    else:
        if len(num_phon) != 12:
            await message.answer(text=_("Допущена помилка",lang))
        else:
            await state.update_data(number_phon=message.text)
            await message.answer(text=_("Заказ оформлено, за додатковою інформацією: @nwrslept",lang), reply_markup=nav.start_kb(lang))

            dict_data_user = await state.get_data()
            list_data_user = []
            for k, v in dict_data_user.items():
                list_data_user.append(v)
            user_id = message.from_user.id
            id_product = list_data_user[0]
            full_name = list_data_user[1]
            index_adress = list_data_user[2]
            number_phon = list_data_user[3]
            user_db.add_user(id_product=id_product, user_id=user_id, full_name=full_name,\
                            index_adress=index_adress, number_phon=number_phon)
            await state.clear()
            input_schedule = int(os.getenv("ADMIN_ID"))
            if message.from_user.id == input_schedule:
                product_for_change = await orm_get_product(session, int(id_product))
                await message.answer_photo(product_for_change.image, caption=f"Користувач @{user} оформив замовлення \
                                     \nФІО: {full_name}\nІндекс та адреса доставки: {index_adress} \
                                     \nНомер телефону: +{num_phon}")
            
                