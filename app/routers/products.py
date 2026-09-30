from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import exceptions as exc
from app import models, schemas
from app.auth import get_current_seller
from app import crud
from app.db_depends import get_async_db
from app.custom_types import PositiveIntPath


router = APIRouter(prefix='/products', tags=['products'])


@router.get('/', response_model=list[schemas.Product])
async def get_products(db: AsyncSession = Depends(get_async_db)):
    """
    Получить список всех активных товаров
    """
    return await crud.products.get_products(db=db)


@router.post('/', response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
async def create_product(
        product_in: schemas.ProductCreate,
        seller: models.User = Depends(get_current_seller),
        db: AsyncSession = Depends(get_async_db),
):
    """
    Создать новый товар, привязанный к текущему продавцу (только для роли seller)
    """
    category_exists = await crud.check_category_exists(db=db, category_id=product_in.category_id)
    if not category_exists:
        raise exc.INVALID_PRODUCT_CATEGORY

    created_product = await crud.create_product(db=db, product_in=product_in, seller_id=seller.id)

    await db.commit()
    return created_product


@router.get('/catedory/{category_id}', response_model=list[schemas.Product])
async def get_products_by_category(
        category_id: PositiveIntPath,
        db: AsyncSession = Depends(get_async_db)
):
    """
    Получить список активных товаров категории
    """
    category_exists = await crud.check_category_exists(db=db, category_id=category_id)
    if not category_exists:
        raise exc.CATEGORY_NOT_FOUND

    return await crud.get_products_by_category(db=db, category_id=category_id)


@router.get('/{product_id}', response_model=schemas.Product)
async def get_product(
        product_id: PositiveIntPath,
        db: AsyncSession = Depends(get_async_db)
):
    """
    Получить информацию об активном товаре по идентификатору
    """
    product = await crud.get_product(db=db, product_id=product_id)
    if product is None:
        raise exc.PRODUCT_NOT_FOUND

    category_exists = await crud.check_category_exists(db=db, category_id=product.category_id)
    if not category_exists:
        raise exc.PRODUCT_CATEGORY_NOT_FOUND

    return product


@router.put('/{product_id}', response_model=schemas.Product)
async def update_product(
        product_id: PositiveIntPath,
        product_in: schemas.ProductUpdate,
        seller: models.User = Depends(get_current_seller),
        db: AsyncSession = Depends(get_async_db),
):
    """
    Обновить товар по идентификатору, если он принадлежит текущему продавцу (только для роли seller)
    """
    product_db = await crud.get_product(db=db, product_id=product_id)
    if product_db is None:
        raise exc.PRODUCT_NOT_FOUND

    if product_db.seller_id != seller.id:
        raise exc.NOT_PRODUCT_OWNER

    if product_in.category_id is not None:
        category_exists = await crud.check_category_exists(db=db, category_id=product_in.category_id)
        if not category_exists:
            raise exc.INVALID_PRODUCT_CATEGORY

    updated_product = await crud.update_product(db=db, product_in=product_in, product_id=product_id)

    await db.commit()
    return updated_product


@router.delete('/{product_id}', response_model=schemas.Product)
async def delete_product(
        product_id: PositiveIntPath,
        seller: models.User = Depends(get_current_seller),
        db: AsyncSession = Depends(get_async_db)
):
    """
    Удалить товар по идентификатору, если он принадлежит текущему продавцу (только для роли seller)
    """
    product_db = await crud.get_product(db=db, product_id=product_id)

    if product_db is None:
        raise exc.PRODUCT_NOT_FOUND

    if product_db.seller_id != seller.id:
        raise exc.NOT_PRODUCT_OWNER

    deleted_product = await crud.delete_product(db=db, product_id=product_id)

    await db.commit()
    return deleted_product
