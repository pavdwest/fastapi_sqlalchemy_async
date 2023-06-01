from typing import List, Dict

from fastapi import APIRouter, status

from src.modules.note.models import Note
from src.modules.note.schemas import NoteCreate, NoteGet


model_class = Note


router = APIRouter(
    tags=[model_class.__tablename_friendly__],
    prefix=f"/{model_class.__tablename__}",
)


@router.post(
    f"/create_one",
    status_code=status.HTTP_200_OK,
    summary=f"Create one {model_class.__name__} in the database.",
    description='Endpoint description. Will use the docstring if not provided.',
)
async def create_one(item: NoteCreate) -> NoteGet:
    tenant = await Note(**item.dict()).create()
    return NoteGet.from_orm(tenant)


@router.get(
    '/get_allx',
    status_code=status.HTTP_200_OK,
    summary='Returns 200 if service is up and running',
    description='Endpoint description. Will use the docstring if not provided.',
)
async def get_allx():
    from sqlalchemy.future import select
    from src.database.service import db

    # Create async session
    session = await db.get_session()

    # Retrieve data
    async with session() as session_context:
        schema_name = 'tenant_386f8f55_8bcb_4151_8dce_035fa7fea31d'
        # await session_context.connection(execution_options={"schema_translate_map": {'tenant': schema_name}})
        await db.set_schema_context(session_context, schema_name)
        q = select(Note)
        res = await session_context.execute(q)
        print(res.scalars())
        return [NoteGet.from_orm(i) for i in res.scalars()]
