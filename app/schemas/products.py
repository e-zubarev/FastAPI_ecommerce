from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, constr


class ProductBase(BaseModel):
    """
    Базовая схема товара с общими валидаторами
    """
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=100,
            description='Название товара от 3 до 100 символов'
        )
    ]
    description: Annotated[
        str | None,
        Field(
            default=None,
            max_length=500,
            description='Описание товара до 500 символов'
        )
    ]
    price: Annotated[
        Decimal,
        Field(
            gt=0,
            description='Цена товара (больше 0)',
            decimal_places=2
        )
    ]
    image_url: Annotated[
        str | None,
        Field(
            default=None,
            max_length=200,
            description='Ссылка на изображение товара'
        )
    ]
    stock: Annotated[
        int,
        Field(
            ge=0,
            description='Количество товара на складе от 0 и больше'
        )
    ]
    category_id: Annotated[
        int,
        Field(description='Идентификатор категории товара')
    ]


class ProductCreate(ProductBase):
    """
    Схема для создания товара (POST /products)
    """
    pass


class ProductUpdate(ProductBase):
    """
    Схема для обновления товара (PUT /products/{product_id})
    """
    pass


class Product(ProductBase):
    """
    Полная схема товара, возвращаемая сервером

    Используется для валидации на выходе в эндпоинтах:
        - GET | POST /products
        - GET | PUT | DELETE /products/{product_id}
        - GET /category/{category_id}
    """
    id: Annotated[
        int,
        Field(description='Уникальный идентификатор товара')
    ]
    created_at: Annotated[
        datetime,
        Field(description='Дата и время создания')
    ]
    updated_at: Annotated[
        datetime | None,
        Field(
            default=None,
            description='Дата и время последнего обновления'
        )
    ]
    is_active: Annotated[
        bool,
        Field(description='Признак активности')
    ]

    model_config = ConfigDict(from_attributes=True)


class ProductList(BaseModel):
    """
    Схема списка товаров с поддержкой пагинации (GET /products)
    """
    items: Annotated[
        list[Product],
        Field(description='Товары текущей страницы')
    ]
    total: Annotated[
        int,
        Field(
            ge=0,
            description='Общее количество товаров'
        )
    ]
    page: Annotated[
        int,
        Field(
            ge=1,
            description='Номер текущей страницы'
        )
    ]
    page_size: Annotated[
        int,
        Field(
            ge=1,
            description='Количество элементов на странице'
        )
    ]

    model_config = ConfigDict(from_attributes=True)


class ProductListFilter(BaseModel):
    """
    Схема входящего фильтра списочного метода товаров (GET /products)
    """
    search: Annotated[
        constr(strip_whitespace=True) | None,
        Field(
            default=None,
            min_length=1,
            description='Строка поиска'
        )
    ]
    category_id: Annotated[
        int | None,
        Field(
            default=None,
            description='Идентификатор категории'
        )
    ]
    min_price: Annotated[
        float | None,
        Field(
            default=None,
            ge=0,
            description='Минимальная цена товара'
        )
    ]
    max_price: Annotated[
        float | None,
        Field(
            default=None,
            ge=0,
            description='Максимальная цена товара'
        )
    ]
    in_stock: Annotated[
        bool | None,
        Field(
            default=None,
            description='True - только товары в наличии, False - только без остатка'
        )
    ]
    seller_id: Annotated[
        int | None,
        Field(
            default=None,
            description='Идентификатор продавца'
        )
    ]
    created_at: Annotated[
        date | None,
        Field(
            default=None,
            description='Дата создания'
        )
    ]
    updated_at: Annotated[
        date | None,
        Field(
            default=None,
            description='Дата последнего обновления'
        )
    ]
