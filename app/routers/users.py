from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import auth
from app import crud
from app import exceptions as exc
from app import models, schemas
from app.db_depends import get_async_db
from app.security import verify_password


router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_in: schemas.UserCreate,
        db: AsyncSession = Depends(get_async_db)
):
    """
    Создать нового пользователя с ролью (buyer/seller)
    """
    email_exists = await crud.check_email_exists(db=db, email=str(user_in.email))
    if email_exists:
        raise exc.EMAIL_ALREADY_EXISTS

    user = await crud.create_user(db=db, user_in=user_in)

    await db.commit()
    return user


@router.post('/token', response_model=schemas.Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_async_db)
):
    """
    Аутентифицировать пользователя и вернуть JWT с email, role и id
    """
    user = await crud.get_user_by_email(db=db, email=form_data.username)
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise exc.INCORRECT_CREDENTIALS

    return auth.generate_tokens_for_user(user)


@router.post('/refresh-token', response_model=schemas.RefreshTokenResponse)
async def refresh_token(user: models.User = Depends(auth.get_current_user_by_refresh)):
    """
    Обновить refresh-токен, принимая старый в теле запроса
    """
    return auth.create_refresh_token_for_user(user)


@router.post('/access-token', response_model=schemas.AccessTokenResponse)
async def access_token(user: models.User = Depends(auth.get_current_user_by_refresh)):
    """
    Обновить access-токен, принимая действующий refresh-токен в теле запроса
    """
    return auth.create_access_token_for_user(user)
