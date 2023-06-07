from sqlalchemy.orm import Mapped, mapped_column

from src.models import AppModel, SharedModelMixin


class Login(AppModel, SharedModelMixin):
    email:             Mapped[str]  = mapped_column(unique=True, nullable=False)
    password_hash:     Mapped[str]  = mapped_column(nullable=False)
    verified:          Mapped[bool] = mapped_column(nullable=False)
    name:              Mapped[str]  = mapped_column(nullable=True)
    surname:           Mapped[str]  = mapped_column(nullable=True)
