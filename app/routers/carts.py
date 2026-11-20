from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import exceptions as exc
from app import models, schemas
from app.auth import get_current_user
from app.db_depends import get_async_db
from app.custom_types import PositiveIntPath


router = APIRouter(prefix='/cart', tags=['cart'])


@router.get('/', response_model=schemas.Cart)
async def get_cart(
        user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)
):
    """
    Получить корзину пользователя
    """
    cart_items = await crud.get_cart_items(db=db, user_id=user.id)

    return schemas.Cart(user_id=user.id, items=cart_items)


@router.post('/items', response_model=schemas.CartItem, status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(
        cart_item: schemas.CartItemCreate,
        user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)
):
    """
    Добавить товар в корзину пользователя
    """
    product_exists = await crud.check_product_exists(db=db, product_id=cart_item.product_id)
    if not product_exists:
        raise exc.PRODUCT_NOT_FOUND

    updated_cart_item = await crud.upsert_cart_item(db=db, cart_item=cart_item, user_id=user.id)

    await db.commit()
    return updated_cart_item


@router.put('/items/{product_id}', response_model=schemas.CartItem)
async def update_cart_item(
        product_id: PositiveIntPath,
        cart_item: schemas.CartItemUpdate,
        user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)
):
    """
    Обновить товар в корзине пользователя
    """
    product_exists = await crud.check_product_exists(db=db, product_id=product_id)
    if not product_exists:
        raise exc.PRODUCT_NOT_FOUND

    updated_cart_item = await crud.update_cart_item(
        db=db, user_id=user.id, product_id=product_id, quantity=cart_item.quantity
    )
    if not updated_cart_item:
        raise exc.CART_ITEM_NOT_FOUND

    await db.commit()
    return updated_cart_item

@router.delete('/items/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_from_cart(
        product_id: PositiveIntPath,
        user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)
):
    """
    Удалить товар из корзины пользователя
    """
    deleted_id = await crud.delete_cart_item(db=db, user_id=user.id, product_id=product_id)
    if not deleted_id:
        raise exc.CART_ITEM_NOT_FOUND

    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(
        user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)
):
    """
    Очистить корзину пользователя
    """
    await crud.delete_cart(db=db, user_id=user.id)

    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
