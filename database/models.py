from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, Numeric, String, Text, func



class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default = func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default = func.now(), onupdate=func.now())

class Schedule(Base):
    __tablename__ = 'schedule'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  
    date: Mapped[str] = mapped_column(nullable=False)
    time: Mapped[str] = mapped_column(nullable=False)
    isbusy: Mapped[bool] = mapped_column(nullable=False)

class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    image: Mapped[str] = mapped_column(String(150))

class Reviews(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(Text)
    image: Mapped[str] = mapped_column(String(150))


class Notes(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(Text)

class Usertable(Base):
    __tablename__ = 'user_table'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_product = Column(Integer)
    user_id = Column(Integer)
    full_name = Column(String)
    index_adress = Column(Integer)
    number_phon = Column(Integer)
    
class Userlang(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    lang = Column(String)


