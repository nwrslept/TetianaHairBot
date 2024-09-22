import os
from aiogram import  F, types, Router
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.state import State, StatesGroup

from database.models import Schedule
from database.orm_query import check_isbusy, orm_add_note, orm_add_product, orm_add_review, orm_add_schedule, orm_delete_note, orm_delete_product, orm_delete_review, orm_delete_schedule, orm_get_notes, orm_get_product, orm_get_products, orm_get_reviews, orm_get_schedule, orm_get_schedules, orm_update_product, orm_update_schedule
from kbds import admin_markups
from kbds.inline import get_callback_btns


admin_router = Router()
class AddProduct(StatesGroup):
    # Шаги состояний
    name = State()
    description = State()
    price = State()
    image = State()

    product_for_change = None

    texts = {
        "AddProduct:name": "Введіть назву заново:",
        "AddProduct:description": "Введіть опис заново:",
        "AddProduct:price": "Введіть вартість заново:",
        "AddProduct:image": "Загрузіть фото заново",
    }

class AddNote(StatesGroup):
    description = State()

    schedule_for_change = None


class AddSchedule(StatesGroup):
    date = State()
    time = State()
    isbusy = State()

    schedule_for_change = None

    texts = {
        'AddSchedule:date': 'Введіть дату заново:',
        'AddSchedule:time': 'Введіть час заново:'
    }

class AddReview(StatesGroup):
    description = State()
    image = State()

    review_for_change = None

    
admin_ids = os.getenv("ADMIN_ID").split(",")
admin_ids = [int(admin_id) for admin_id in admin_ids]



@admin_router.message(Command('admin'))
async def admin_cmd(message: types.Message):
    if message.from_user.id in admin_ids:

        await message.answer("Адмін панель: ",  reply_markup=admin_markups.admin_kb.as_markup(
                              resize_keyboard=True,
                              input_field_placeholder='Що вас цікавить?'))
        


@admin_router.message(F.text == "Список продуктів")
async def starring_at_product(message: types.Message, session: AsyncSession):
    if message.from_user.id in admin_ids:

        for product in await orm_get_products(session):
            await message.answer_photo(
                product.image,
                caption=f"{product.name}\
                    \n{product.description}\nВартість: {round(product.price, 2)}kč",
                reply_markup=get_callback_btns(
                    btns={
                        "Видалити": f"delete_{product.id}",
                        "Змінити": f"change_{product.id}",
                    }
                ),
            )
    await message.answer("Ось список продуктів ⏫")

@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_product_callback(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    await orm_delete_product(session, int(product_id))

    await callback.answer("Товар видалено!")
    await callback.message.answer("Товар видалено!")




@admin_router.message(F.text.lower() == "дати записів")
async def schedule_list(message: types.Message, session: AsyncSession):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        schedules = await check_isbusy(session)
        if schedules:  # Якщо є доступні дати
            for schedule in schedules:
                    await message.answer(f"Доступна дата: \n{schedule.date}\n{schedule.time}",
                                 reply_markup=get_callback_btns(btns={
                                     'Видалити': f'deleteschedule_{schedule.id}',
                                     'Змінити': f'changeschedule_{schedule.id}',
                                 }))

@admin_router.callback_query(F.data.startswith('deleteschedule_'))
async def delete_schedule(callback: types.callback_query, session: AsyncSession):
    schedule_id= callback.data.split("_")[-1]
    await orm_delete_schedule(session, int(schedule_id))

    await callback.answer('Дату видалено')
    await callback.message.answer('Дату видалено!')


@admin_router.message(F.text == "Список відгуків")
async def starring_at_review(message: types.Message, session: AsyncSession):
    if message.from_user.id in admin_ids:


        for review in await orm_get_reviews(session):
            await message.answer_photo(
            review.image,
            caption=f"{review.description}",
            reply_markup=get_callback_btns(
                btns={
                    "Видалити": f"deletereview_{review.id}",
                }
            ),
        )

@admin_router.callback_query(F.data.startswith('deletereview_'))
async def delete_review(callback: types.callback_query, session: AsyncSession):
    review_id= callback.data.split("_")[-1]
    await orm_delete_review(session, int(review_id))
    await callback.answer('Відгук видалено')
    await callback.message.answer('Відгук видалено!')



@admin_router.message(F.text == "Переглянути замітки")
async def starring_at_notes(message: types.Message, session: AsyncSession):
    if message.from_user.id in admin_ids:

        for note in await orm_get_notes(session):
            await message.answer(
                f"{note.description}",
                reply_markup=get_callback_btns(
                btns={
                    "Видалити": f"deletenote_{note.id}",
                }
            ),
        )
            
@admin_router.callback_query(F.data.startswith('deletenote_'))
async def delete_note(callback: types.callback_query, session: AsyncSession):
    review_id= callback.data.split("_")[-1]
    await orm_delete_note(session, int(review_id))
    await callback.answer('Замітку видалено')
    await callback.message.answer('Замітку видалено!')

 #FSM



@admin_router.message(StateFilter(None),F.text == 'Добавити відгук')
async def add_review(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_ids:
        await message.answer('Введіть опис відгуку', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(AddReview.description)

@admin_router.message(AddReview.description)
async def add_image_review(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Загрузіть зображення")
    await state.set_state(AddReview.image)

@admin_router.message(AddReview.image)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):

    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
        
    await orm_add_review(session, data)
    await message.answer("Відгук добавлено", reply_markup=admin_markups.admin_kb.as_markup(
                              resize_keyboard=True,
                              input_field_placeholder='Що вас цікавить?'))
    await state.clear()
        


@admin_router.callback_query(StateFilter(None), F.data.startswith("changeschedule_"))
async def change_schedule_callback(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    schedule_id = callback.data.split("_")[-1]

    schedule_for_change = await orm_get_schedule(session, int(schedule_id))

    AddSchedule.schedule_for_change = schedule_for_change

    await callback.answer()
    await callback.message.answer(
        "Введіть дату в форматі хх.хх.хххх", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddSchedule.date)

@admin_router.message(StateFilter(None),F.text == 'Добавити дату для запису')
async def add_schedule(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_ids:
        await message.answer('Введіть дату в форматі xx.xx.xxxx', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(AddSchedule.date)


@admin_router.message(AddSchedule.date, or_f(F.text, F.text == '.'))
async def add_date(message: types.Message, state: FSMContext):
    if message.text =='.':
        await state.update_data(date=AddSchedule.schedule_for_change.date)
    else:
        await state.update_data(date=message.text)
    await message.answer('Введіть час в форматі хх:xx')
    await state.set_state(AddSchedule.time)


@admin_router.message(AddSchedule.time, or_f(F.text, F.text=='.'))
async def add_time(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(isbusy=False)

    if message.text =='.':
        await state.update_data(time=AddSchedule.schedule_for_change.time)
    else:
        await state.update_data(time=message.text)
        data = await state.get_data()
        if AddSchedule.schedule_for_change:
            await orm_update_schedule(session, AddSchedule.schedule_for_change.id, data)
        else:
            await orm_add_schedule(session, data)
        await message.answer('Дату та час добавлено', reply_markup=admin_markups.admin_kb.as_markup(resize_keyboard=True))
        await state.clear()
    AddSchedule.schedule_for_change = None



@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_product_callback(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    product_id = callback.data.split("_")[-1]

    product_for_change = await orm_get_product(session, int(product_id))

    AddProduct.product_for_change = product_for_change

    await callback.answer()
    await callback.message.answer(
        "Введіть назву продукту", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter(None), F.text == "Добавити продукт")
async def add_product(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_ids:

        await message.answer(
            "Введіть назву продукту", reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(AddProduct.name)


@admin_router.message(StateFilter("*"), Command("відміна"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "відміна")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    if AddProduct.product_for_change:
        AddProduct.product_for_change = None
    await state.clear()
    await message.answer("Дії відмінено", reply_markup=admin_markups.admin_kb.as_markup(
                              resize_keyboard=True,
                              input_field_placeholder='Що вас цікавить?'))


@admin_router.message(StateFilter("*"), Command("назад"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer(
            'Попереднього кроку немає, або введіть назву, або напишіть "відміна"'
        )
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"Ви повернулись до попереднього кроку \n {AddProduct.texts[previous.state]}"
            )
            return
        previous = step


@admin_router.message(AddProduct.name, or_f(F.text, F.text == "."))
async def add_name(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(name=AddProduct.product_for_change.name)
    else:
        if len(message.text) >= 100:
            await message.answer(
                "Назва продукту не має перевишати 100 символів. \n Введіть заново"
            )
            return

        await state.update_data(name=message.text)
    await message.answer("Введіть опис продукту")
    await state.set_state(AddProduct.description)


@admin_router.message(AddProduct.name)
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer("Ви ввели не допустимі данні, введіть текст назви продукту")


@admin_router.message(AddProduct.description, or_f(F.text, F.text == "."))
async def add_description(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(description=AddProduct.product_for_change.description)
    else:
        await state.update_data(description=message.text)
    await message.answer("Введіть вартість товару")
    await state.set_state(AddProduct.price)


@admin_router.message(AddProduct.description)
async def add_description2(message: types.Message, state: FSMContext):
    await message.answer("Ви ввели не допустимі данні, введіть текст опису продукту")


@admin_router.message(AddProduct.price, or_f(F.text, F.text == "."))
async def add_price(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(price=AddProduct.product_for_change.price)
    else:
        try:
            float(message.text)
        except ValueError:
            await message.answer("Введіть коректне значення ціни")
            return

        await state.update_data(price=message.text)
    await message.answer("Загрузіть зображення продукту")
    await state.set_state(AddProduct.image)


@admin_router.message(AddProduct.price)
async def add_price2(message: types.Message, state: FSMContext):
    await message.answer("Ви ввели не допустимі данні, введіть вартість товару")


@admin_router.message(AddProduct.image, or_f(F.photo, F.text == "."))
async def add_image_product(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text and message.text == ".":
        await state.update_data(image=AddProduct.product_for_change.image)

    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if AddProduct.product_for_change:
            await orm_update_product(session, AddProduct.product_for_change.id, data)
        else:
            await orm_add_product(session, data)
        await message.answer("Продукт добавлено/змінено", reply_markup=admin_markups.admin_kb.as_markup(
                              resize_keyboard=True,
                              input_field_placeholder='Що вас цікавить?'))
        await state.clear()

    except Exception as e:
        await message.answer(
            f"Помилка: \n{str(e)}",
            reply_markup=admin_markups.admin_kb.as_markup(
                              resize_keyboard=True,
                              input_field_placeholder='Що вас цікавить?')),
        
        await state.clear()

    AddProduct.product_for_change = None


@admin_router.message(AddProduct.image)
async def add_image2(message: types.Message, state: FSMContext):
    await message.answer("Відправте фото")



@admin_router.message(StateFilter(None),F.text == 'Добавити замітку')
async def add_note(message: types.Message, state: FSMContext):
    if message.from_user.id in admin_ids:
        await message.answer('Введіть замітку', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(AddNote.description)

@admin_router.message(AddNote.description)
async def add_descriptionnote(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await orm_add_note(session, data)
    await message.answer("Замітку добавлено", reply_markup=admin_markups.admin_kb.as_markup(
                              resize_keyboard=True,
                              input_field_placeholder='Що вас цікавить?'))
    await state.clear()



