from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import Integer, DateTime, func
import asyncio

engine = create_async_engine(url='postgresql+asyncpg://postgres:12345@localhost/WordCountingTgBot_db')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)  # Убедитесь, что ID уникален
    request_count: Mapped[int] = mapped_column(Integer, default=0)  # Счетчик запросов
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())  # Дата регистрации
async def async_main():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "main":
    asyncio.run(async_main())