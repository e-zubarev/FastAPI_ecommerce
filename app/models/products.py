from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Computed,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    func,
    text
)
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Product(Base):
    """
    Модель SQLAlchemy для работы с таблицей товаров
    """
    __tablename__ = 'products'

    __table_args__ = (
        Index('idx_products_tsv_gin', 'tsv', postgresql_using='gin'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(500))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    image_url: Mapped[str | None] = mapped_column(String(200))
    stock: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    seller_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    rating: Mapped[float] = mapped_column(Float, default=0.0, server_default=text('0'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    tsv: Mapped[TSVECTOR] = mapped_column(
        TSVECTOR,
        Computed(
            '''
            setweight(to_tsvector('russian', coalesce(name, '')), 'A')
            || 
            setweight(to_tsvector('russian', coalesce(description, '')), 'B')
            ''',
            persisted=True
        ),
        nullable=False
    )

    category: Mapped['Category'] = relationship('Category', back_populates='products', single_parent=True)
    seller: Mapped['User'] = relationship('User', back_populates='products')
    cart_items: Mapped[list['CartItem']] = relationship('CartItem', back_populates='product', cascade='all, delete-orphan')
