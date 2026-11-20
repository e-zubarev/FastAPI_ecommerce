from collections.abc import Sequence
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, computed_field

from .products import Product


class CartItemBase(BaseModel):
    """
    Базовая схема товара в корзине
    """
    product_id: Annotated[
        int,
        Field(
            ge=1,
            description='Идентификатор товара'
        )
    ]
    quantity: Annotated[
        int,
        Field(
            ge=0,
            default=1,
            description='Количество товара'
        )
    ]


class CartItemCreate(CartItemBase):
    """
    Схема добавления нового товара в корзину (POST /cart/item)
    """
    pass


class CartItemUpdate(BaseModel):
    """
    Схема обновления количества товара корзине (PUT /cart/item/{product_id})
    """
    quantity: Annotated[
        int,
        Field(
            ge=0,
            default=1,
            description='Новое количество товара'
        )
    ]


class CartItem(BaseModel):
    """
    Полная схема товара в корзине, возвращаемая сервером
    """
    id: Annotated[
        int,
        Field(description='Идентификатор позиции в корзине')
    ]
    product: Annotated[
        Product,
        Field(description='Информация о товаре')
    ]
    quantity: Annotated[
        int,
        Field(
            ge=0,
            default=1,
            description='Количество товара'
        )
    ]

    model_config = ConfigDict(from_attributes=True)


class Cart(BaseModel):
    """
    Полная схема всей корзины товаров, возвращаемая сервером
    """
    user_id: Annotated[
        int,
        Field(description='Идентификатор пользователя')
    ]
    items: Annotated[
        Sequence[CartItem],
        Field(
            default_factory=list,
            description='Список позиций в корзине'
        )
    ]

    @computed_field(description='Общее количество товаров')
    @property
    def total_quantity(self) -> int:
        return sum(item.quantity for item in self.items)

    @computed_field(description='Общая стоимость товаров')
    @property
    def total_price(self) -> Decimal:
        return sum(
            (item.quantity * item.product.price or Decimal('0') for item in self.items),
            start=Decimal('0')
        )

    model_config = ConfigDict(from_attributes=True)
