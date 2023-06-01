from sqlalchemy import Column, Integer, String

from src.models import AppModel, SharedModelMixin


class Book(SharedModelMixin, AppModel):
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)
