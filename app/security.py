from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app import config


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Преобразовать пароль в хеш
    """
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверить, соответствует ли введенный пароль сохраненному хешу
    """
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Создать access-токен
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode['exp'] = expire
    to_encode['token_type'] = 'access'
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """
    Создать refresh-токен
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode['exp'] = expire
    to_encode['token_type'] = 'refresh'
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
