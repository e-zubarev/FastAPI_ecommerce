from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    """ Базовая схема категорий с общими валидаторами для схем категорий """
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
            description='Название категории от 3 до 50 символов'
        )
    ]
    parent_id: Annotated[
        int | None,
        Field(
            default=None,
            description='Идентификатор родительской категории, None - для корневой категории'
        )
    ]


class CategoryCreate(CategoryBase):
    """ Схема для создания категории (POST) """
    pass


class CategoryUpdate(CategoryBase):
    """ Схема для обновления категории (PUT) """
    pass


class Category(CategoryBase):
    """ Схема категории для ответа в GET-запросе"""
    id: Annotated[
        int,
        Field(description='Уникальный идентификатор категории')
    ]
    is_active: Annotated[
        bool,
        Field(description='Признак активности')
    ]

    model_config = ConfigDict(from_attributes=True)
