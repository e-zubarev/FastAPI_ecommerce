from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CartItem(Base):
    """
    Модель SQLAlchemy для работы с таблицей корзины товаров
    """
    __tablename__ = 'cart_items'

    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='uq_cart_items_user_product'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'), index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    user: Mapped['User'] = relationship('User', back_populates='cart_items')
    product: Mapped['Product'] = relationship('Product', back_populates='cart_items')
