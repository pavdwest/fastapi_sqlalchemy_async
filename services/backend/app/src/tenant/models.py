import uuid
from asyncio import current_task

from sqlalchemy import Column, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_scoped_session
from sqlalchemy.orm import sessionmaker

from src.database.service import db
from src.models import AppModel, IdentifierMixin, SharedModelMixin


def generate_schema_name() -> str:
    """
    Generates a string of the form 'tenant_889a0da2_e5c7_461d_b1b2_b6f6828eea34'

    Returns:
        str: the result
    """
    return f"tenant_{str(uuid.uuid4()).replace('-','_')}"


class Tenant(IdentifierMixin, SharedModelMixin, AppModel):
    schema_name = Column(String, default=generate_schema_name)

    async def activate(self, session_context: AsyncSession) -> None:
        await session_context.connection(execution_options={"schema_translate_map": {'tenant': self.schema_name}})

    async def provision(self):
        if self.schema_name is not None:
            # Direct - no schema
            db.create_db_schema(schema_name=self.schema_name)

            # # Create schema tables
            # session = async_scoped_session(
            #     sessionmaker(
            #         bind=db.async_engine,
            #         expire_on_commit=False,
            #         class_=AsyncSession
            #     ),
            #     scopefunc=current_task
            # )

            # conn = await session.connection()
            # await conn.execution_options(schema_translate_map={None: self.schema_name})
            # # await conn.run_sync(self.metadata.drop_all)
            # await conn.run_sync(self.metadata.create_all)
            # await conn.close()



            # engine = await db.get_engine()

            # conn = engine.connect().execution_options(
            #     schema_translate_map={
            #         'shared': None,
            #         'tenant': self.schema_name,
            #     }
            # )

            # from src.modules.note.models import Note
            # item = await Note(
            #     name='TEST',
            #     author='asdsadsa',
            #     release_year=1999,
            # ).create()
            # conn.close()



            # item = await Note(
            #     name='TEST',
            #     author='asdsadsa',
            #     release_year=1999,
            # ).create()

            # schema_translate_map={
            #     'shared': None,
            #     'tenant': self.schema_name,
            # }


            # async with db.async_session() as session:
            #     conn = await db.async_session.connection()
            #     await conn.execution_options(
            #         schema_translate_map={
            #             'shared': None,
            #             'tenant': self.schema_name,
            #         }
            #     )
            #     await conn.run_sync(self.__class__.metadata.create_all)

            # session = db.get_async_session()

            # async with session.begin():
            #     c = await session.connection(
            #         execution_options={
            #             'schema_translate_map': {
            #                 'shared': None,
            #                 'tenant': self.schema_name,
            #             }
            #         }
            #     )
            #     c.run_sync(self.__class__.metadata.create_all)
