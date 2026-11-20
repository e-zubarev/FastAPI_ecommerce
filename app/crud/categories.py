from collections.abc import Sequence

from sqlalchemy import exists, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def get_categories(db: AsyncSession) -> Sequence[models.Category]:
    """
    Получить список всех активных категорий
    """
    stmt = (
        select(models.Category)
        .where(models.Category.is_active)
    )

    categories = await db.scalars(stmt)

    return categories.all()


async def check_category_exists(
        db: AsyncSession,
        *,
        category_id: int
) -> bool:
    """
    Проверить существование активной категории
    """
    stmt = select(
        exists()
        .where(
            models.Category.id == category_id,
            models.Category.is_active
        )
    )

    return await db.scalar(stmt)


async def create_category(
        db: AsyncSession,
        *,
        category_in: schemas.CategoryCreate
) -> models.Category:
    """
    Создать новую категорию
    """
    stmt = (
        insert(models.Category)
        .values(**category_in.model_dump())
        .returning(models.Category)
    )

    return await db.scalar(stmt)


async def update_category(
        db: AsyncSession,
        *,
        category_id: int,
        category_in: schemas.CategoryUpdate
) -> models.Category:
    """
    Обновить категорию по идентификатору
    """
    stmt = (
        update(models.Category)
        .where(models.Category.id == category_id)
        .values(**category_in.model_dump(exclude_unset=True))
        .returning(models.Category)
    )

    return await db.scalar(stmt)


async def delete_category(
        db: AsyncSession,
        category_id: int
) -> models.Category:
    """
    Удалить активную категорию по идентификатору, установив поле is_active в False
    """
    stmt = (
        update(models.Category)
        .where(
            models.Category.id == category_id,
            models.Category.is_active
        )
        .values(is_active=False)
        .returning(models.Category)
    )

    return await db.scalar(stmt)
