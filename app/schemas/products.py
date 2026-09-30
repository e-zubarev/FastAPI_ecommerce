from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """ Базовая схема продукта с общими валидаторами для схем продуктов """
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
    """ Схема для создания продукта (POST) """
    pass


class ProductUpdate(ProductBase):
    """ Схема для обновления продукта (PUT) """
    pass


class Product(ProductBase):
    """ Схема продукта для ответа в GET-запросе """
    id: Annotated[
        int,
        Field(description='Уникальный идентификатор товара')
    ]
    is_active: Annotated[
        bool,
        Field(description='Признак активности')
    ]

    model_config = ConfigDict(from_attributes=True)
