from collections.abc import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Предоставляет асинхронную сессию SQLAlchemy для работы с базой данных PostgreSQL.
    Автоматически откатывает транзакцию в случае ошибки
    """
    async with async_session_maker() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
