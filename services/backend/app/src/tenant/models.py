from typing import Any
import uuid

from sqlalchemy import Column, String, Select, Insert, Update, Delete, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import TENANT_SCHEMA_NAME
from src.database.service import db
from src.models import AppModel, IdentifierMixin, SharedModelMixin


TENANT_SCHEMA_NAME_PREFIX = 'tenant_'


def generate_schema_name() -> str:
    """
    Generates a string of the form 'tenant_889a0da2_e5c7_461d_b1b2_b6f6828eea34'

    Returns:
        str: the result
    """
    return f"{TENANT_SCHEMA_NAME_PREFIX}{str(uuid.uuid4()).replace('-','_')}"


class Tenant(AppModel, IdentifierMixin, SharedModelMixin):
    schema_name = Column(String, default=generate_schema_name)

    async def execute_query(
        self,
        query: Select | Insert |  Update | Delete,
        session: AsyncSession = None,
    ) -> Any | Result:
        return await db.execute_query(
            query=query,
            schema_name=self.schema_name,
            session=session,
        )

    async def activate(self, session_context: AsyncSession) -> None:
        await db.set_schema_context(session_context, self.schema_name)

    async def provision(self):
        if self.schema_name is not None:
            # Create a new schema for the tenant
            db.create_db_schema(schema_name=self.schema_name)

            # Create schema tables
            db.clone_db_schema(source_schema_name=TENANT_SCHEMA_NAME, target_schema_name=self.schema_name)

    @classmethod
    def schema_name_from_identifier(cls, identifier: str) -> str:
        return f"{TENANT_SCHEMA_NAME_PREFIX}{identifier}"

    @classmethod
    def identifier_from_schema_name(cls, schema_name: str) -> str:
        return schema_name.removeprefix(TENANT_SCHEMA_NAME_PREFIX)
