from sqlalchemy import Column, Integer, String

from src.models import AppModel, TenantModelMixin


# tenant_022ed83f_efe7_4724_9496_04b2327b5761

class Note(TenantModelMixin, AppModel):
# class Note(AppModel):
    # __table_args__ = { 'schema': 'tenant_386f8f55_8bcb_4151_8dce_035fa7fea31d' }
    # __table_args__ = { 'schema': None }

    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)
