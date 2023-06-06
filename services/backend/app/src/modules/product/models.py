from typing import List

from sqlalchemy import Column, Integer
from sqlalchemy.orm import Mapped, relationship

from src.models import AppModel, TenantModelMixin, IdentifierMixin, DescriptionMixin


class Product(AppModel, TenantModelMixin, IdentifierMixin, DescriptionMixin):
    release_year = Column(Integer, nullable=False)

    # Relations
    orders: Mapped[List['Order']] = relationship(
        back_populates='product',
        cascade='all, delete-orphan',
    )
