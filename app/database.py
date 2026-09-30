from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import DATABASE_URL


# Создание объекта Engine (управляет подключением к БД и пулом соединений)
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Настройка фабрики сессий с привязкой к Engine
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# Базовый класс для ORM моделей SqlAlchemy
class Base(DeclarativeBase):
    pass
