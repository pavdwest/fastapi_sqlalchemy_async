from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.modules.product.models import Product
from src.models import AppModel, TenantModelMixin, GUIDMixin, DescriptionMixin, TimestampMixin


class Order(AppModel, TenantModelMixin, TimestampMixin, DescriptionMixin, GUIDMixin):
    product_id: Mapped[int]     = mapped_column(BigInteger, ForeignKey(Product.id))
    product:    Mapped[Product] = relationship(back_populates='orders')
    client:     Mapped[str]     = mapped_column(nullable=False)
    quantity:   Mapped[int]     = mapped_column(nullable=False)
    unit_price: Mapped[float]   = mapped_column(nullable=False)
    amount:     Mapped[float]   = mapped_column(nullable=False)
