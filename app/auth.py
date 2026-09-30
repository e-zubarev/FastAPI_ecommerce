import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app import config
from app import exceptions as exc
from app import models, schemas
from app.crud import get_user_by_email
from app.db_depends import get_async_db
from app import security


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/token')


def _get_user_payload(user: models.User) -> dict:
    """
    Внутренний хелпер для формирования payload токенов
    """
    return {'sub': user.email, 'role': user.role, 'id': user.id}


def create_access_token_for_user(user: models.User) -> str:
    """
    Создать access-токен с помощью модели пользователя
    """
    return security.create_access_token(data=_get_user_payload(user))


def create_refresh_token_for_user(user: models.User) -> str:
    """
    Создать refresh-токен с помощью модели пользователя
    """
    return security.create_refresh_token(data=_get_user_payload(user))


def generate_tokens_for_user(user: models.User) -> schemas.Token:
    """
    Собрать полную пару токенов
    """
    return schemas.Token(
        access_token=create_access_token_for_user(user),
        refresh_token=create_refresh_token_for_user(user),
        token_type='bearer'
    )


def create_access_token_response(user: models.User) -> schemas.AccessTokenResponse:
    """
    Сборка схемы ответа для обновления только access-токена
    """
    return schemas.AccessTokenResponse(
        access_token=create_access_token_for_user(user),
        token_type='bearer'
    )


def create_refresh_token_response(user: models.User) -> schemas.RefreshTokenResponse:
    """
    Сборка схемы ответа для обновления только refresh-токена
    """
    return schemas.RefreshTokenResponse(
        refresh_token=create_refresh_token_for_user(user),
        token_type='bearer'
    )


async def get_current_user_by_refresh(
        body: schemas.RefreshTokenRequest,
        db: AsyncSession = Depends(get_async_db)
) -> models.User:
    """
    Проверить refresh-токен из тела запроса и вернуть текущего пользователя
    """
    try:
        payload = jwt.decode(body.refresh_token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        email: str | None = payload.get('sub')
        token_type: str | None = payload.get('token_type')

        if email is None or token_type != 'refresh':
            raise exc.INVALID_REFRESH_TOKEN
    except jwt.ExpiredSignatureError:
        raise exc.REFRESH_TOKEN_EXPIRED
    except jwt.PyJWTError:
        raise exc.INVALID_REFRESH_TOKEN

    user = await get_user_by_email(db=db, email=email)
    if user is None:
        raise exc.INVALID_REFRESH_TOKEN

    return user


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_async_db)
) -> models.User:
    """
    Проверить access-токен и вернуть текущего пользователя
    """
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        email: str | None = payload.get('sub')
        token_type: str | None = payload.get('token_type')

        if email is None or token_type != 'access':
            raise exc.INVALID_CREDENTIALS

    except jwt.ExpiredSignatureError:
        raise exc.ACCESS_TOKEN_EXPIRED
    except jwt.PyJWTError:
        raise exc.INVALID_CREDENTIALS

    user = await get_user_by_email(db=db, email=email)
    if user is None:
        raise exc.INVALID_CREDENTIALS

    return user


async def get_current_buyer(user: models.User = Depends(get_current_user)) -> models.User:
    """
    Проверить access-токен и наличие у пользователя роли покупателя
    """
    if user.role != 'buyer':
        raise exc.BUYER_ONLY
    return user


async def get_current_seller(user: models.User = Depends(get_current_user)) -> models.User:
    """
    Проверить access-токен и наличие у пользователя роли продавца
    """
    if user.role != 'seller':
        raise exc.SELLER_ONLY
    return user


async def allow_admin(user: models.User = Depends(get_current_user)):
    """
    Проверить access-токен и наличие у пользователя роли администратора
    """
    if user.role != 'admin':
        raise exc.ADMIN_ONLY
