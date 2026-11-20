from collections.abc import Sequence

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app import models, schemas


async def get_product_rating(
        db: AsyncSession,
        *,
        product_id: int
) -> float:
    """
    Посчитать средний рейтинг товара по активным отзывам
    """
    stmt = (
        select(
            func.coalesce(func.avg(models.Review.grade), 0.0)
        )
        .where(
            models.Review.product_id == product_id,
            models.Review.is_active
        )
    )

    return await db.scalar(stmt)


async def get_review(
        db: AsyncSession,
        *,
        review_id: int
) -> models.Review | None:
    """
    Получить активный отзыв по идентификатору
    """
    stmt = (
        select(models.Review)
        .where(
            models.Review.id == review_id,
            models.Review.is_active
        )
    )

    return await db.scalar(stmt)


async def get_reviews(db: AsyncSession) -> Sequence[models.Review]:
    """
    Получить список активных отзывов
    """
    stmt = (
        select(models.Review)
        .where(models.Review.is_active)
    )

    reviews = await db.scalars(stmt)

    return reviews.all()


async def get_reviews_by_product(
        db: AsyncSession,
        *,
        product_id: int
) -> Sequence[models.Review]:
    """
    Получить список активных отзывов товара
    """
    stmt = (
        select(models.Review)
        .where(
            models.Review.product_id == product_id,
            models.Review.is_active
        )
    )

    reviews = await db.scalars(stmt)

    return reviews.all()


async def create_review(
        db: AsyncSession,
        *,
        review_in: schemas.ReviewCreate,
        buyer_id: int
) -> models.Review:
    """
    Создать отзыв о товаре
    """
    stmt = (
        insert(models.Review)
        .values(
            **review_in.model_dump(),
            user_id=buyer_id
        )
        .returning(models.Review)
    )

    return await db.scalar(stmt)


async def delete_review(
        db: AsyncSession,
        *,
        review_id: int
) -> models.Review | None:
    """
    Удалить активный отзыв по идентификатору, установив поле is_active в False
    """
    stmt = (
        update(models.Review)
        .where(
            models.Review.id == review_id,
            models.Review.is_active
        )
        .values(is_active=False)
        .returning(models.Review)
    )

    return await db.scalar(stmt)
