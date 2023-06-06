from typing import List

from sqlalchemy import Column, Integer
from sqlalchemy.orm import Mapped, relationship

from src.models import AppModel, TenantModelMixin, IdentifierMixin, DescriptionMixin


class Product(AppModel, TenantModelMixin, IdentifierMixin, DescriptionMixin):
    orders: Mapped[List['Order']] = relationship(
        back_populates='product',
        cascade='all, delete-orphan',
    )
    release_year = Column(Integer, nullable=False)
