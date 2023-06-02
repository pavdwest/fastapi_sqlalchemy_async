from typing import List, Dict

from fastapi import APIRouter, status
from sqlalchemy.future import select
from src.database.service import db

from src.modules.note.models import Note
from src.modules.note.validators import NoteCreate, NoteGet


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
    schema_name = 'tenant_386f8f55_8bcb_4151_8dce_035fa7fea31d'
    db_item = await Note(**item.dict()).create(schema_name)
    return NoteGet.from_orm(db_item)


@router.get(
    '/get_all',
    status_code=status.HTTP_200_OK,
    summary='Returns 200 if service is up and running',
    description='Endpoint description. Will use the docstring if not provided.',
)
async def get_all() -> List[NoteGet]:
    # Get tenant
    from src.tenant.models import Tenant
    tenant: Tenant = (await db.execute_query(select(Tenant).limit(1))).scalar_one()

    q = select(Note)
    res = await tenant.execute_query(q)
    return [NoteGet.from_orm(i) for i in res.scalars()]

    # # Get tenant's
    # q = select(Note)
    # res = await db.execute_query(q, schema_name='tenant_386f8f55_8bcb_4151_8dce_035fa7fea31d')
    # return [NoteGet.from_orm(i) for i in res.scalars()]
    # q = select(Note).where(Note.id > 0)
    # res = await tenant.execute_query(query=q)
    # return [NoteGet.from_orm(i) for i in res.scalars()]

    # schema_name = 'tenant_386f8f55_8bcb_4151_8dce_035fa7fea31d'
    # q = select(Note).where(Note.id > 3)
    # res = await db.execute_query(
    #     query=q,
    #     schema_name=schema_name
    # )
    # return [NoteGet.from_orm(i) for i in res.scalars()]


    # schema_name = 'tenant_386f8f55_8bcb_4151_8dce_035fa7fea31d'
    # res = await Note.fetch_all(schema_name)
    # return [NoteGet.from_orm(i) for i in res]
