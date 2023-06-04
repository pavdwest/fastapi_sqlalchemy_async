from typing import Any, AsyncGenerator

from sqlalchemy import create_engine, Select, Insert, Update, Delete, Result, ScalarResult
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_scoped_session, async_sessionmaker, async_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.schema import CreateSchema

from src.logging.service import logger
from src.config import (
    SHARED_SCHEMA_NAME,
    TENANT_SCHEMA_NAME,
    DATABASE_POOL_SIZE,
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_URL_SYNC,
    DATABASE_URL_ASYNC
)


class DatabaseService:
    def __init__(self) -> None:
        self.__class__.init_db()
        self.async_engine: AsyncEngine = create_async_engine(
            DATABASE_URL_ASYNC,
            future=True,
            echo=True,
            pool_size=DATABASE_POOL_SIZE,
            pool_pre_ping=True,
        )

    @classmethod
    def create_db_if_not_exists(cls):
        if not database_exists(url=DATABASE_URL_SYNC):
            logger.warning(f"Creating database: '{DATABASE_HOST}/{DATABASE_NAME}'...")
            create_database(url=DATABASE_URL_SYNC)

            if not database_exists(url=DATABASE_URL_SYNC):
                raise Exception(f"COULD NOT CREATE DATABASE '{DATABASE_HOST}/{DATABASE_NAME}'!")
            else:
                logger.warning('Database created.')
                logger.warning('Creating default schemas...')
                cls.create_db_schema(SHARED_SCHEMA_NAME)
                cls.create_db_schema(TENANT_SCHEMA_NAME)
                logger.warning('Default schemas created.')
        else:
            logger.info(f"Database '{DATABASE_HOST}/{DATABASE_NAME}' already exists. Nothing to do.")

    @classmethod
    def drop_database(cls, database_url: str):
        logger.warning("Dropping database: '{DATABASE_HOST}/{DATABASE_NAME}'")

        if database_exists(url=database_url):
            drop_database(url=database_url)
        else:
            logger.warning(f"Database '{DATABASE_HOST}/{DATABASE_NAME}' doesn't exist. Nothing to do.")

    @classmethod
    def create_db_schema(cls, schema_name: str) -> None:
        """
        Creates a new blank schema with the provided name, which can then be accessed as e.g.

        ```
        select * from 'schema_name'.some_table
        ```

        Args:
            schema_name (str): Schema name
        """
        sync_engine = create_engine(DATABASE_URL_SYNC)
        with sync_engine.begin() as conn:
            if not conn.dialect.has_schema(conn, schema_name):
                logger.warning(f"Creating schema: '{schema_name}'...")
                conn.execute(CreateSchema(schema_name))
                if not conn.dialect.has_schema(conn, schema_name):
                    logger.error(f"Could not create schema: '{schema_name}'.")
            else:
                logger.info(f"Schema '{schema_name}' already exists.")

        sync_engine.dispose()


    @classmethod
    def clone_db_schema(source_schema_name: str, target_schema_name: str) -> None:
        sync_engine = create_engine(DATABASE_URL_SYNC)
        with sync_engine.begin() as conn:
            # logger.warning(f"Cloning schema '{source_schema_name}' to '{target_schema_name}...")
            # conn.execute()

            # # res = cursor.execute(f"create table if not exists {target_schema_name}.{table_name} (like {source_schema_name}.{table_name} including all)")
            # TODO
            pass

        sync_engine.dispose()

    @classmethod
    def init_db(cls):
        cls.create_db_if_not_exists()

    async def get_session(self) -> AsyncSession:
        """
        Creates and returns a new session on the database.

        Returns:
            AsyncSession: The newly created session
        """
        return async_sessionmaker(
            self.async_engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    async def set_schema_context(self, session_context: AsyncSession, schema_name: str = SHARED_SCHEMA_NAME) -> None:
        """
        Mutates a session to point at a specific database schema

        Args:
            session_context (AsyncSession): The session
            schema_name (str): _description_
        """
        options = {}
        if schema_name == SHARED_SCHEMA_NAME:
            options['schema_translate_map'] = { 'tenant': None }
        else:
            options['schema_translate_map'] = { 'tenant': schema_name, 'shared': None }

        await session_context.connection(
            execution_options=options
        )

    async def execute_query(
        self,
        query: Select | Insert |  Update | Delete,
        schema_name: str = SHARED_SCHEMA_NAME,
        session: AsyncSession = None
    ) -> Any | Result:
        """
        Utility method to execute a single query in a simple way. Example:

        ```
        # Simple way
        q = select(Note)
        res = await db.execute_query(schema_name='tenant_386f8f55_8bcb_4151_8dce_035fa7fea31d', query=q)

        # The above is equivalent to
        session: AsyncSession = await db.get_session()

        async with session() as session_context:
            schema_name = 'tenant_386f8f55_8bcb_4151_8dce_035fa7fea31d'
            await db.set_schema_context(session_context, schema_name)
            q = select(Note).where(Note.id > 5)
            res = await session_context.execute(q)

        Args:
            query (Select | Insert | Update | Delete): The query to execute
            schema_name (str, optional): Defaults to SHARED_SCHEMA_NAME.
            session (AsyncSession, optional): Can pass in an existing session. A new one will be generated if omitted.
        ```

        Returns:
            Any | Result: _description_
        """
        if session is None:
            session: AsyncSession = await db.get_session()

        async with session() as session:
            await self.set_schema_context(session, schema_name)
            res = await session.execute(query)
            await session.commit()
            return res

    async def shutdown(self):
        if self.async_engine is not None:
            await self.async_engine.dispose()

db: DatabaseService = DatabaseService()


# from sqlalchemy.future import select
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
#
#
# class AsyncDatabaseManager:
#     def __init__(self, schema_name):
#         self.schema_name = schema_name
#         self.async_engine = None
#         self.session = None
#         self.conn = None

#     async def __aenter__(self):
#         self.async_engine = create_async_engine(
#             DATABASE_URL_ASYNC,
#             future=True,
#             echo=True,
#             pool_size=50,
#             pool_pre_ping=True,
#         )

#         self.session = async_sessionmaker(
#             bind=self.async_engine,
#             expire_on_commit=False,
#             class_=AsyncSession,
#         )

#         async with self.session() as session_context:
#             await session_context.connection(
#                 execution_options={"schema_translate_map": {'tenant': self.schema_name, None: self.schema_name}}
#             )
#             return session_context

#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         if self.conn:
#             self.conn.close()
#             self.conn = None
#         if self.session:
#             # await self.session.close()
#             self.session = None
#         if self.async_engine:
#             await self.async_engine.dispose()
#             self.async_engine = None


## Manual from scratch select
# from sqlalchemy.future import select
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
# from sqlalchemy.orm import sessionmaker

# from src.config import DATABASE_URL_ASYNC


# # Create async database engine
# async_engine: AsyncEngine = create_async_engine(
#     DATABASE_URL_ASYNC,
#     future=True,
#     echo=True,
#     pool_size=50,
#     pool_pre_ping=True,
# )

# # Create async session
# session = async_sessionmaker(
#     async_engine,
#     expire_on_commit=False,
#     class_=AsyncSession
# )

# # Retrieve data
# async with session() as session_context:
#     schema_name = 'tenant_386f8f55_8bcb_4151_8dce_035fa7fea31d'
#     await session_context.connection(execution_options={"schema_translate_map": {'tenant': schema_name}})
#     q = select(Note)
#     res = await session_context.execute(q)
#     print(res.scalars())
#     return [NoteGet.from_orm(i) for i in res.scalars()]
