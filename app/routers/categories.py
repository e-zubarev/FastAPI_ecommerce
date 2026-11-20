from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import exceptions as exc
from app import schemas
from app.auth import allow_admin
from app import crud
from app.db_depends import get_async_db
from app.custom_types import PositiveIntPath


router = APIRouter(
    prefix='/categories',
    tags=['categories']
)


@router.get('/', response_model=list[schemas.Category])
async def get_categories(db: AsyncSession = Depends(get_async_db)):
    """
    Получить список всех активных категорий
    """
    return await crud.get_categories(db=db)


@router.post(
    '/',
    response_model=schemas.Category,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(allow_admin)]
)
async def create_category(
        category_in: schemas.CategoryCreate,
        db: AsyncSession = Depends(get_async_db)
):
    """
    Создать новую категорию
    """
    if category_in.parent_id is not None:
        parent_exists = await crud.check_category_exists(db=db, category_id=category_in.parent_id)
        if not parent_exists:
            raise exc.PARENT_CATEGORY_NOT_FOUND

    created_category = await crud.create_category(db=db, category_in=category_in)

    await db.commit()
    return created_category


@router.put(
    '/{category_id}',
    response_model=schemas.Category,
    dependencies=[Depends(allow_admin)]
)
async def update_category(
        category_id: PositiveIntPath,
        category_in: schemas.CategoryUpdate,
        db: AsyncSession = Depends(get_async_db)
):
    """
    Обновить категорию по идентификатору
    """
    category_exists = await crud.check_category_exists(db=db, category_id=category_id)
    if category_exists is None:
        raise exc.CATEGORY_NOT_FOUND

    if category_in.parent_id is not None:
        parent_exists = await crud.check_category_exists(db=db, category_id=category_in.parent_id)
        if not parent_exists:
            raise exc.PARENT_CATEGORY_NOT_FOUND
        if category_in.parent_id == category_id:
            raise exc.CYCLIC_CATEGORY_DEPENDENCY

    updated_category = await crud.update_category(db=db, category_id=category_id, category_in=category_in)

    await db.commit()
    return updated_category


@router.delete(
    '/{category_id}',
    response_model=schemas.Category,
    dependencies=[Depends(allow_admin)]
)
async def delete_category(
        category_id: PositiveIntPath,
        db: AsyncSession = Depends(get_async_db)
):
    """
    Удалить категорию по идентификатору (установить is_active=False)
    """
    category_exists = await crud.check_category_exists(db=db, category_id=category_id)
    if not category_exists:
        raise exc.CATEGORY_NOT_FOUND

    deleted_category = await crud.delete_category(db=db, category_id=category_id)

    await db.commit()
    return deleted_category
