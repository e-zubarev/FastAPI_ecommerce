from .categories import router as categories
from .products import router as products
from .users import router as users
from .reviews import router as reviews
from .carts import router as carts

__all__ = [
    'categories',
    'products',
    'users',
    'reviews',
    'carts'
]
