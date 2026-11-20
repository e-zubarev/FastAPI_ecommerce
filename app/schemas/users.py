from typing import Annotated, Literal

from pydantic import BaseModel, Field, ConfigDict, EmailStr, SecretStr


class UserBase(BaseModel):
    """
    Базовая схема пользователя с общими валидаторами
    """
    email: Annotated[
        EmailStr,
        Field(description='Электронная почта пользователя')
    ]
    role: Annotated[
        Literal['buyer', 'seller'],
        Field(
            default='buyer',
            description='Роль: "buyer" или "seller"'
        )
    ]


class UserCreate(UserBase):
    """
    Схема для создания пользователя (POST /users)
    """
    password: Annotated[
        SecretStr,
        Field(min_length=8, description='Пароль пользователя')
    ]


class User(UserBase):
    """
    Полная схема пользователя, возвращаемая сервером

     Используется в эндпоинтах:
        - POST /users
    """
    id: Annotated[
        int,
        Field(description='Уникальный идентификатор пользователя')
    ]
    is_active: Annotated[
        bool,
        Field(description='Признак активности')
    ]
    role: Annotated[
        Literal['buyer', 'seller', 'admin'],
        Field(
            default='buyer',
            description='Роль: "buyer", "seller" или "admin"'
        )
    ]

    model_config = ConfigDict(from_attributes=True)


class TokenBaseResponse(BaseModel):
    """
    Базовая схема с общими валидаторами для токенов, возвращаемых сервером
    """
    token_type: Annotated[str, Field(default='bearer', description='Тип токена (по умолчанию bearer)')]


class Token(TokenBaseResponse):
    """
    Полная схема, состоящая из access и refresh токенов, возвращаемая сервером (POST /token)
    """
    access_token: Annotated[
        str,
        Field(description='Новый access-токен')
    ]
    refresh_token: Annotated[
        str,
        Field(description='Новый refresh-токен')
    ]


class RefreshTokenRequest(BaseModel):
    """
    Схема входящего запроса обновления с refresh-токеном в теле

    Используется в эндпоинтах:
        - POST /refresh-token
        - POST /access-token
    """
    refresh_token: Annotated[
        str,
        Field(description='Действующий refresh-токен')
    ]


class RefreshTokenResponse(TokenBaseResponse):
    """
    Схема ответа обновления refresh-токена, возвращаемая сервером (POST /refresh-token)
    """
    refresh_token: Annotated[
        str,
        Field(description='Новый refresh-токен')
    ]


class AccessTokenResponse(TokenBaseResponse):
    """
    Схема ответа обновления access-токена, возвращаемая сервером (POST /access-token)
    """
    access_token: Annotated[
        str,
        Field(description='Новый access-токен')
    ]
