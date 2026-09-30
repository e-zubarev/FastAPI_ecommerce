from .categories import router as categories
from .products import router as products
from .users import router as users
from .reviews import router as reviews

__all__ = [
    'categories',
    'products',
    'users',
    'reviews',
]
