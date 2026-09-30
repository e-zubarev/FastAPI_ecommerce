from typing import Annotated, Literal

from pydantic import BaseModel, Field, ConfigDict, EmailStr, SecretStr


class UserBase(BaseModel):
    """ Базовая схема пользователя с общими полями """
    email: Annotated[
        EmailStr,
        Field(
            description='Электронная почта пользователя',
            pattern='^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        )
    ]
    role: Annotated[
        Literal['buyer', 'seller'],
        Field(
            default='buyer',
            description='Роль: "buyer" или "seller"'
        )
    ]


class UserCreate(UserBase):
    """ Схема для создания пользователя в POST-запросе """
    password: Annotated[SecretStr, Field(min_length=8, description='Пароль пользователя')]


class User(UserBase):
    """ Схема пользователя для ответа в GET-запросе """
    id: Annotated[int, Field(description='Уникальный идентификатор пользователя')]
    is_active: Annotated[bool, Field(description='Признак активности')]
    role: Annotated[
        Literal['buyer', 'seller', 'admin'],
        Field(
            default='buyer',
            description='Роль: "buyer", "seller" или "admin"'
        )
    ]

    model_config = ConfigDict(from_attributes=True)


class TokenBaseResponse(BaseModel):
    """ Базовая схема ответа для токенов с общими полями """
    token_type: Annotated[str, Field(default='bearer', description='Тип токена (по умолчанию bearer)')]


class Token(TokenBaseResponse):
    """ Схема полной пары токенов при логине """
    access_token: Annotated[str, Field(description='Новый access-токен')]
    refresh_token: Annotated[str, Field(description='Новый refresh-токен')]


class RefreshTokenRequest(BaseModel):
    """ Схема запроса обновления с refresh-токеном в теле """
    refresh_token: Annotated[str, Field(description='Действующий refresh-токен')]


class RefreshTokenResponse(TokenBaseResponse):
    """ Схема ответа обновления refresh-токена """
    refresh_token: Annotated[str, Field(description='Новый refresh-токен')]


class AccessTokenResponse(TokenBaseResponse):
    """ Схема ответа обновления access-токена """
    access_token: Annotated[str, Field(description='Новый access-токен')]
