import math
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Base, Notes, Product, Reviews, Schedule, Userlang, Usertable

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker




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
        description=data["description"],
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



async def orm_add_review(session: AsyncSession, data: dict):
    obj = Reviews(
        description=data["description"],
        image=data["image"],
    )
    session.add(obj)
    await session.commit()


async def orm_get_reviews(session: AsyncSession):
    query = select(Reviews)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_review(session: AsyncSession, review_id: int):
    query = select(Reviews).where(Reviews.id == review_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_review(session: AsyncSession, review_id: int, data):
    query = update(Reviews).where(Reviews.id == review_id).values(
        description=data["description"],
        image=data["image"],)
    await session.execute(query)
    await session.commit()


async def orm_delete_review(session: AsyncSession, review_id: int):
    query = delete(Reviews).where(Reviews.id == review_id)
    await session.execute(query)
    await session.commit()


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