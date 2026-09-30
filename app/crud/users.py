from sqlalchemy import exists, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.security import hash_password


async def check_email_exists(
        db: AsyncSession,
        *,
        email: str
) -> bool:
    """
    Проверить, существует ли пользователь с переданным email
    """
    stmt = (
        select(
            exists()
            .where(models.User.email == email)
        )
    )

    return await db.scalar(stmt)


async def get_user_by_email(
        db: AsyncSession,
        *,
        email: str
) -> models.User | None:
    """
    Получить активного пользователя по email
    """
    stmt = (
        select(models.User)
        .where(
            models.User.email == email,
            models.User.is_active
        )
    )

    return await db.scalar(stmt)


async def create_user(
        db: AsyncSession,
        *,
        user_in: schemas.UserCreate
) -> models.User:
    """
    Создать нового пользователя
    """
    stmt = (
        insert(models.User)
        .values(
            email=user_in.email,
            hashed_password=hash_password(user_in.password.get_secret_value()),
            role=user_in.role
        )
        .returning(models.User)
    )

    return await db.scalar(stmt)
