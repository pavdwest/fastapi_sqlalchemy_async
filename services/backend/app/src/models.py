from __future__ import annotations
import uuid
from functools import lru_cache
from typing import List
from datetime import datetime

from inflection import titleize, pluralize, underscore
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped, mapped_column,
)
from sqlalchemy.future import select
from sqlalchemy import BigInteger, Column, Identity
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import get_class_by_table

from src.logging.service import logger
from src.config import SHARED_SCHEMA_NAME, TENANT_SCHEMA_NAME
from src.database.service import db


class IdMixin:
    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)

class TimestampMixin:
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class TimestampsMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)


class IdentifierMixin:
    identifier: Mapped[str] =  mapped_column(unique=True)


class DescriptionMixin:
    description: Mapped[str] =  mapped_column(unique=False)


class GUIDMixin:
    guid: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)


class SharedModelMixin:
    __table_args__ = { 'schema': SHARED_SCHEMA_NAME }


class TenantModelMixin:
    __table_args__ = { 'schema': TENANT_SCHEMA_NAME }


class AppModel(DeclarativeBase, IdMixin, TimestampsMixin):
    @declared_attr
    @lru_cache(maxsize=1)
    def __tablename__(cls):
        return underscore(cls.__name__)

    @classmethod
    @lru_cache(maxsize=1)
    def get_model_class(cls):
        return get_class_by_table(cls, cls.__table__)

    @declared_attr
    @lru_cache(maxsize=1)
    def __tablename_friendly__(cls):
        return pluralize(titleize(cls.__tablename__))

    @classmethod
    async def init_orm(cls):
        # await cls.drop_tables()
        # await cls.create_tables()
        pass

    @classmethod
    async def create_tables(cls, schema_name: str = SHARED_SCHEMA_NAME):
        session = await db.get_session()
        async with session.begin() as session_ctx:
            await db.set_schema_context(session_ctx, schema_name)
            conn = await session_ctx.connection()
            logger.warning('Creating tables...')
            await conn.run_sync(cls.metadata.create_all)
            logger.warning('Tables created.')

    @classmethod
    async def drop_tables(cls, schema_name = SHARED_SCHEMA_NAME):
        session = await db.get_session()
        async with session.begin() as session_ctx:
            await db.set_schema_context(session_ctx, schema_name)
            conn = await session_ctx.connection()
            logger.warning('Dropping tables...')
            await conn.run_sync(cls.metadata.drop_all)
            logger.warning('Tables dropped.')

    async def create(self, schema_name: str = SHARED_SCHEMA_NAME) -> AppModel:
        """
        Persists this instance to the database.

        Args:
            schema_name (str, optional): Defaults to SHARED_SCHEMA_NAME.

        Returns:
            AppModel: Updated self
        """
        session = await db.get_session()
        async with session.begin() as session_ctx:
            await db.set_schema_context(session_ctx, schema_name)
            session_ctx.add(self)
            return self

    @classmethod
    async def fetch_all(cls, schema_name: str = SHARED_SCHEMA_NAME) -> List[AppModel]:
        """
        Retrieves all of the records in the database.

        Args:
            schema_name (str, optional): Defaults to SHARED_SCHEMA_NAME.

        Returns:
            List[AppModel]: _description_
        """
        session = await db.get_session()
        async with session.begin() as session_ctx:
            await db.set_schema_context(session_ctx, schema_name)
            q = select(cls.get_model_class())
            res = await session_ctx.execute(q)
            return [i for i in res.scalars()]
