from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.DB_URL)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


# Пример создания сессии для работы с бд, в поле execute будет какой-то код на выполнение.
# session = async_session_maker()
# await session.execute()

# # Запрос для наглядности и не более (работа с сырыми запросами)
# async def func():
#     async with engine.begin() as conn:
#         res = await conn.execute(text("SELECT version()"))
#         print(res.fetchone())
#
#
# asyncio.run(func())
