from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app import exceptions as exc
from app import models, schemas
from app.auth import get_current_buyer, get_current_user
from app.db_depends import get_async_db
from app.custom_types import PositiveIntPath


router = APIRouter(tags=['reviews'])


@router.get('/reviews/', response_model=list[schemas.Review])
async def get_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Получить список активных отзывов
    """
    return await crud.get_reviews(db=db)


@router.get('/products/{product_id}/reviews/', response_model=list[schemas.Review])
async def get_reviews_by_product(
        product_id: PositiveIntPath,
        db: AsyncSession = Depends(get_async_db)
):
    """
    Получить список активных отзывов товара
    """
    product_exists = await crud.check_product_exists(db=db, product_id=product_id)
    if not product_exists:
        raise exc.PRODUCT_NOT_FOUND

    return await crud.get_reviews_by_product(db=db, product_id=product_id)


@router.post('/reviews/', response_model=schemas.Review)
async def create_review(
        review_in: schemas.ReviewCreate,
        buyer: models.User = Depends(get_current_buyer),
        db: AsyncSession = Depends(get_async_db)
):
    """
    Создать отзыв о товаре
    """
    try:
        review = await crud.create_review(db=db, review_in=review_in, buyer_id=buyer.id)

        rating = await crud.get_product_rating(db=db, product_id=review_in.product_id)
        await crud.update_product_rating(db=db, product_id=review_in.product_id, rating=rating)

        await db.commit()
        return review

    except IntegrityError as e:
        await db.rollback()

        error_msg = str(e.orig).lower()

        if 'uq_user_product_active_review' in error_msg:
            raise exc.DUPLICATE_REVIEW
        if 'product_id' in error_msg:
            raise exc.PRODUCT_NOT_FOUND

        raise exc.DB_INTEGRITY_VIOLATED


@router.delete('/reviews/{review_id}', response_model=schemas.Review)
async def delete_review(
        review_id: PositiveIntPath,
        user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_db)
):
    """
    Удалить отзыв по идентификатору, установив поле is_active в False.
    Доступно только владельцу отзыва или пользователю с ролью администратора
    """
    review = await crud.get_review(db=db, review_id=review_id)
    if not review:
        raise exc.REVIEW_NOT_FOUND

    is_owner = user.id == review.user_id
    is_admin = user.role == 'admin'
    if not (is_owner or is_admin):
        raise exc.NOT_REVIEW_OWNER

    deleted_review = await crud.delete_review(db=db, review_id=review_id)
    if not deleted_review:
        raise

    rating = await crud.get_product_rating(db=db, product_id=int(deleted_review.product_id))
    await crud.update_product_rating(db=db, product_id=int(deleted_review.product_id), rating=rating)

    await db.commit()
    return deleted_review
