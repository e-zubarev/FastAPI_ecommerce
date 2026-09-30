from typing import Sequence

from sqlalchemy import exists, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def get_products(db: AsyncSession) -> Sequence[models.Product]:
    """
    Получить список активных товаров
    """
    stmt = (
        select(models.Product)
        .join(models.Category)
        .where(models.Product.is_active)
    )

    products = await db.scalars(stmt)

    return products.all()


async def get_products_by_category(
        db: AsyncSession,
        *,
        category_id: int
) -> Sequence[models.Product]:
    """
    Получить список активных товаров категории
    """
    stmt = (
        select(models.Product)
        .where(
            models.Product.category_id == category_id,
            models.Product.is_active
        )
    )

    products = await db.scalars(stmt)

    return products.all()


async def get_product(
        db: AsyncSession,
        *,
        product_id: int
) -> models.Product | None:
    """
    Получить информацию об активном товаре по идентификатору
    """
    stmt = (
        select(models.Product)
        .where(
            models.Product.id == product_id,
            models.Product.is_active
        )
    )

    return await db.scalar(stmt)


async def check_product_exists(
        db: AsyncSession,
        *,
        product_id: int
) -> bool:
    """
    Проверить существование активного товара
    """
    stmt = (
        select(
            exists().where(
                models.Product.id == product_id,
                models.Product.is_active
            )
        )
    )

    return await db.scalar(stmt)


async def create_product(
        db: AsyncSession,
        *,
        product_in: schemas.ProductCreate,
        seller_id: int
) -> schemas.Product:
    """
    Создать новый товар
    """
    stmt = (
        insert(models.Product)
        .values(
            **product_in.model_dump(),
            seller_id=seller_id
        )
        .returning(models.Product)
    )

    return await db.scalar(stmt)


async def update_product(
        db: AsyncSession,
        *,
        product_id: int,
        product_in: schemas.ProductUpdate
) -> models.Product | None:
    """
    Обновить товар по идентификатору
    """
    stmt = (
        update(models.Product)
        .where(models.Product.id == product_id)
        .values(**product_in.model_dump(exclude_unset=True))
        .returning(models.Product)
    )

    return await db.scalar(stmt)


async def update_product_rating(
        db: AsyncSession,
        *,
        product_id: int,
        rating: float
) -> None:
    """
    Обновить средний рейтинг товара
    """
    stmt = (
        update(models.Product)
        .where(
            models.Product.id == product_id,
            models.Product.is_active
        )
        .values(rating=round(rating, 2))
    )

    await db.execute(stmt)


async def delete_product(
        db: AsyncSession,
        *,
        product_id: int
) -> models.Product | None:
    """
    Удалить товар по идентификатору, установив поле is_active в False
    """
    stmt = (
        update(models.Product)
        .where(models.Product.id == product_id)
        .values(is_active=False)
        .returning(models.Product)
    )

    return await db.scalar(stmt)
