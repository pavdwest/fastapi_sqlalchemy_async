from typing import List, Dict

from fastapi import APIRouter, status
from sqlalchemy.future import select
from inflection import pluralize

from src.database.service import db
from src.tenant.models import Tenant
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
async def create_one(tenant_identifier: str, item: NoteCreate) -> NoteGet:
    schema_name = Tenant.schema_name_from_identifier(tenant_identifier)
    db_item = await Note(**item.dict()).create(schema_name)
    return NoteGet.from_orm(db_item)


@router.get(
    '/get_all',
    status_code=status.HTTP_200_OK,
    summary=f"Get all {pluralize(model_class.__name__)} from the database.",
    description='Endpoint description. Will use the docstring if not provided.',
)
async def get_all(tenant_identifier: str) -> List[NoteGet]:
    schema_name = Tenant.schema_name_from_identifier(tenant_identifier)
    res = await Note.fetch_all(schema_name)
    return [NoteGet.from_orm(i) for i in res]


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    summary=f"Get one {model_class.__name__} from the database.",
    description='Endpoint description. Will use the docstring if not provided.',
)
async def get_one_by_id(tenant_identifier: str, id: int) -> NoteGet:
    schema_name = Tenant.schema_name_from_identifier(tenant_identifier)
    res = await Note.get(id, schema_name)
    return NoteGet.from_orm(res)
