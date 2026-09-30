from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    """ Базовая схема отзыва о товаре """
    product_id: Annotated[
        int,
        Field(description='Идентификатор товара')
    ]
    grade: Annotated[
        int,
        Field(
            ge=1,
            le=5,
            description='Оценка товара (от 1 до 5)'
        )
    ]
    comment: Annotated[
        str | None,
        Field(
            default=None,
            description='Текст отзыва'
        )
    ]


class ReviewCreate(ReviewBase):
    """ Схема для валидации входящего отзыва о товаре в POST запросе """
    pass


class Review(ReviewBase):
    """ Схема отзыва о товаре, используемая в GET запросе """
    id: Annotated[
        int,
        Field(description='Уникальный идентификатор идентификатор отзыва о товаре')
    ]
    comment_date: Annotated[
        datetime,
        Field(description='Дата отзыва')
    ]
    user_id: Annotated[
        int,
        Field(description='Идентификатор пользователя')
    ]
    is_active: Annotated[
        bool,
        Field(description='Признак активности')
    ]

    model_config = ConfigDict(from_attributes=True)
