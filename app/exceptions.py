from fastapi import HTTPException, status

# Исключения для аутентификации

ACCESS_TOKEN_EXPIRED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Access token has expired',
    headers={'WWW-Authenticate': 'Bearer'}
)

ADMIN_ONLY = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Only administrators can perform this action'
)

BUYER_ONLY = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Only buyers can perform this action'
)

EMAIL_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Email already registered'
)

INCORRECT_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Incorrect email or password',
    headers={'WWW-Authenticate': 'Bearer'}
)

INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'}
)

INVALID_REFRESH_TOKEN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate refresh token',
    headers={'WWW-Authenticate': 'Bearer'}
)

REFRESH_TOKEN_EXPIRED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Refresh token has expired',
    headers={'WWW-Authenticate': 'Bearer'}
)

SELLER_ONLY = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Only sellers can perform this action'
)


# Исключения для категорий

CATEGORY_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Category not found or inactive'
)

CYCLIC_CATEGORY_DEPENDENCY = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Category cannot be its own parent'
)

INVALID_PRODUCT_CATEGORY = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Product category not found or inactive'
)

PARENT_CATEGORY_NOT_FOUND = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Parent category not found or inactive'
)

PRODUCT_CATEGORY_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Product category not found or inactive'
)


# Исключения для товаров

NOT_PRODUCT_OWNER = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='You can only modify your own products'
)

PRODUCT_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Product not found or inactive'
)

INVALID_PRICE_RANGE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Минимальная цена не может быть больше максимальной",
)


# Исключения для отзывов

DUPLICATE_REVIEW = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="You have already reviewed this product. You can only edit your existing review."
)

NOT_REVIEW_OWNER = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='You do not have permission to delete this review'
)

REVIEW_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Review not found or inactive"
)


# Исключения для корзины

CART_ITEM_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Cart item not found'
)


# Исключения базы данных

DB_INTEGRITY_VIOLATED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Database integrity constraints violated."
)
