from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Actions, Base, Cart, Notes, Product, Schedule, Userlang, Usertable

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, Session, joinedload




async def orm_add_schedule(session: AsyncSession, data: dict):
        obj = Schedule(
            date=data['date'],
            time=data['time'],
            isbusy=data['isbusy']
            )
        session.add(obj)
        await session.commit()

async def orm_get_schedules(session: AsyncSession):
    query = select(Schedule)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_schedule(session: AsyncSession, schedule_id: int):
    query = select(Schedule).where(Schedule.id == schedule_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_schedule(session: AsyncSession, schedule_id: int, data):
    query = update(Schedule).where(Schedule.id == schedule_id).values(
        date=data["date"],
        time=data["time"],
        isbusy=data["isbusy"],
        )
    await session.execute(query)
    await session.commit()


async def orm_delete_schedule(session: AsyncSession, schedule_id: int):
    query = delete(Schedule).where(Schedule.id == schedule_id)
    await session.execute(query)
    await session.commit()






async def orm_add_product(session: AsyncSession, data: dict):
    obj = Product(
        name=data["name"],
        namecz=data["namecz"],
        description=data["description"],
        descriptioncz=data["descriptioncz"],
        price=float(data["price"]),
        image=data["image"],
    )
    session.add(obj)
    await session.commit()


async def orm_get_products(session: AsyncSession):
    query = select(Product)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_product(session: AsyncSession, product_id: int):
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_product(session: AsyncSession, product_id: int, data):
    query = update(Product).where(Product.id == product_id).values(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"],)
    await session.execute(query)
    await session.commit()


async def orm_delete_product(session: AsyncSession, product_id: int):
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()





async def add_to_cart(user_id: int, product_id: int, quantity: int, session: AsyncSession):
    # Перевіряємо, чи цей товар вже є в кошику
    existing_cart_item = await session.execute(
        select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    )
    cart_item = existing_cart_item.scalar_one_or_none()

    if cart_item:
        # Якщо товар вже в кошику, оновлюємо кількість
        cart_item.quantity += quantity
    else:
        # Якщо товару ще немає в кошику, додаємо новий запис
        new_cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        session.add(new_cart_item)

    await session.commit()


async def remove_from_cart(user_id: int, product_id: int, session: AsyncSession):
    # Шукаємо товар у кошику
    cart_item = await session.execute(
        select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    )
    cart_item = cart_item.scalar_one_or_none()

    if cart_item:
        # Видаляємо товар з кошика
        await session.delete(cart_item)
        await session.commit()
    else:
        print("Товар не знайдено в кошику.")

async def get_cart(user_id: int, session: Session):
    cart_items = await session.execute(
        select(Cart).where(Cart.user_id == user_id).options(joinedload(Cart.product))
    )
    return cart_items.scalars().all()  # Повертаємо всі товари у кошику

async def clear_cart(user_id: int, session: AsyncSession):
    # Отримуємо всі продукти з кошика користувача
    cart_items = await session.execute(
        select(Cart).where(Cart.user_id == user_id)
    )
    cart_items = cart_items.scalars().all()  # Отримуємо всі товари у кошику

    for item in cart_items:
        await remove_from_cart(user_id, item.product_id, session)  # Видаляємо кожен товар з кошика







async def orm_add_note(session: AsyncSession, data: dict):
    obj = Notes(
        description=data["description"],
    )
    session.add(obj)
    await session.commit()

async def orm_get_notes(session: AsyncSession):
    query = select(Notes)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_note(session: AsyncSession, note_id: int):
    query = select(Notes).where(Notes.id == note_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_delete_note(session: AsyncSession, note_id: int):
    query = delete(Notes).where(Notes.id == note_id)
    await session.execute(query)
    await session.commit()

async def check_isbusy(session: AsyncSession):
    
    async with session.begin():
        result = await session.execute(
            select(Schedule).filter_by(isbusy=False)
        )
        schedules = result.scalars().all()

        return schedules
    
async def orm_add_action(session: AsyncSession, data: dict):
    obj = Actions(
        description=data["description"],
        descriptioncz=data["descriptioncz"],

    )
    session.add(obj)
    await session.commit()

async def orm_get_actions(session: AsyncSession):
    query = select(Actions)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_action(session: AsyncSession, action_id: int):
    query = select(Actions).where(Actions.id == action_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_delete_action(session: AsyncSession, action_id: int):
    query = delete(Actions).where(Actions.id == action_id)
    await session.execute(query)
    await session.commit()
    


class Database:
    def __init__(self, db_file):
        self.engine = create_engine(f'sqlite:///{db_file}')
        Base.metadata.create_all(self.engine)  # Створення таблиць, якщо їх немає
        self.Session = sessionmaker(bind=self.engine)

    def user_exists(self, user_id):
        with self.Session() as session:
            result = session.execute(select(Userlang).where(Userlang.user_id == user_id)).scalars().all()
            return len(result) > 0
        
    def add_user(self, user_id, lang):
        with self.Session() as session:
            new_user = Userlang(user_id=user_id, lang=lang)
            session.add(new_user)
            session.commit()
            
    def get_all_user_ids(self):
        with self.Session() as session:
            result = session.execute(select(Userlang.user_id))
            user_ids = [row[0] for row in result.fetchall()]
            return user_ids
        
    def get_lang(self, user_id):
        with self.Session() as session:
            result = session.execute(select(Userlang.lang).where(Userlang.user_id == user_id)).scalar()
            return result
        
    def update_lang(self, user_id, new_lang):
        with self.Session() as session:
            stmt = update(Userlang).where(Userlang.user_id == user_id).values(lang=new_lang)
            session.execute(stmt)
            session.commit()

class UserDB:
    def __init__(self, db_file='my_base.db'):
        self.engine = create_engine(f'sqlite:///{db_file}')
        Base.metadata.create_all(self.engine)  # Створення таблиці, якщо її немає
        self.Session = sessionmaker(bind=self.engine)

    def add_user(self, id_product, user_id, full_name, index_adress, number_phon):
        with self.Session() as session:
            new_user = Usertable(
                id_product=id_product,
                user_id=user_id,
                full_name=full_name,
                index_adress=index_adress,
                number_phon=number_phon
            )
            session.add(new_user)
            session.commit()

user_db = UserDB()


