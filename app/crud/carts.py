from collections.abc import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import Insert, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import models, schemas


async def get_cart_items(
        db: AsyncSession,
        *,
        user_id: int
) -> Sequence[models.CartItem]:
    """
    Получить все позиции корзины пользователя
    """
    stmt = (
        select(models.CartItem)
        .where(models.CartItem.user_id == user_id)
        .order_by(models.CartItem.id)
        .options(selectinload(models.CartItem.product))
    )

    cart_items = await db.scalars(stmt)

    return cart_items.all()

async def upsert_cart_item(
        db: AsyncSession,
        *,
        cart_item: schemas.CartItemCreate,
        user_id: int
) -> models.CartItem:
    """
    Добавить или обновить позицию корзины пользователя (upsert)
    """
    stmt: Insert = (
        insert(models.CartItem)
        .values(
            user_id=user_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        .options(selectinload(models.CartItem.product))
    )
    final_stmt = stmt.on_conflict_do_update(
        index_elements=['user_id', 'product_id'],
        set_={'quantity': models.CartItem.quantity + cart_item.quantity},
    ).returning(models.CartItem)

    return await db.scalar(final_stmt)

async def update_cart_item(
        db: AsyncSession,
        *,
        user_id: int,
        product_id: int,
        quantity: int
) -> models.CartItem | None:
    """
    Обновить позицию корзины пользователя
    """
    stmt = (
        update(models.CartItem)
        .where(
            models.CartItem.user_id == user_id,
            models.CartItem.product_id == product_id
        )
        .values(quantity=quantity)
        .returning(models.CartItem)
        .options(selectinload(models.CartItem.product))
    )

    return await db.scalar(stmt)

async def delete_cart_item(
        db: AsyncSession,
        *,
        user_id: int,
        product_id: int
) -> int | None:
    """
    Удалить позицию корзины по идентификатору товара и пользователя
    """
    stmt = (
        delete(models.CartItem)
        .where(
            models.CartItem.user_id == user_id,
            models.CartItem.product_id == product_id
        )
        .returning(models.CartItem.id)
    )

    return await db.scalar(stmt)

async def delete_cart(
        db: AsyncSession,
        *,
        user_id: int
) -> None:
    """
    Удалить корзину пользователя
    """
    stmt = (
        delete(models.CartItem)
        .where(models.CartItem.user_id == user_id)
    )

    await db.execute(stmt)
