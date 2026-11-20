from datetime import timedelta
from collections.abc import Sequence

from sqlalchemy import desc, exists, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def get_products(
        db: AsyncSession,
        *,
        page: int,
        page_size: int,
        filters: schemas.ProductListFilter
) -> tuple[int, Sequence[models.Product]]:
    """
    Получить список активных товаров и общее число записей (для списка с пагинацией)
    """
    where_clause: list = [models.Product.is_active == True]

    rank_column = None

    if filters.search and filters.search != '':
        ts_query = func.websearch_to_tsquery('russian', filters.search)
        where_clause.append(models.Product.tsv.op('@@')(ts_query))
        rank_column = func.ts_rank_cd(models.Product.tsv, ts_query).label('rank')

    if filters.category_id:
        where_clause.append(models.Product.category_id == filters.category_id)

    if filters.min_price:
        where_clause.append(models.Product.price >= filters.min_price)

    if filters.max_price:
        where_clause.append(models.Product.price <= filters.max_price)

    if filters.in_stock is not None:
        where_clause.append(models.Product.stock > 0 if filters.in_stock else models.Product.stock == 0)

    if filters.seller_id:
        where_clause.append(models.Product.seller_id == filters.seller_id)

    if filters.created_at:
        where_clause.append(filters.created_at <= models.Product.created_at < filters.created_at + timedelta(days=1))

    if filters.updated_at:
        where_clause.append(filters.updated_at <= models.Product.updated_at < filters.updated_at + timedelta(days=1))

    total_stmt = select(func.count(models.Product.id)).where(*where_clause)
    total = await db.scalar(total_stmt)

    if rank_column is not None:
        select_clause = [models.Product, rank_column]
        order_clause = [desc('rank'), models.Product.id]
    else:
        select_clause = [models.Product]
        order_clause = [models.Product.id]

    products_stmt = (
        select(*select_clause)
        .where(*where_clause)
        .order_by(*order_clause)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    products = await db.execute(products_stmt)
    products = products.scalars().all()

    return total, products


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
) -> models.Product:
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
