from sqlalchemy import Column, Integer, String

from src.models import AppModel, TenantModelMixin, IdentifierMixin, DescriptionMixin


class Product(AppModel, TenantModelMixin, IdentifierMixin, DescriptionMixin):
    release_year = Column(Integer, nullable=False)
