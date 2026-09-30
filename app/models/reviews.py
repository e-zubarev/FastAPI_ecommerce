from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Index,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Review(Base):
    """
    Модель SQLAclhemy для работы с таблицей отзывов
    """
    __tablename__ = 'reviews'

    __table_args__ = (
        Index(
            'uq_user_product_active_review',
            'user_id', 'product_id',
            unique=True,
            postgresql_where=text('is_active = true')
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)
    comment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    grade: Mapped[int] = mapped_column(SmallInteger, CheckConstraint('grade >= 1 AND grade <= 5'), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
