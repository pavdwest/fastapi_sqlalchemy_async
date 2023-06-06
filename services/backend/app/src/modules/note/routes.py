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
async def create_one(tenant_schema: str, item: NoteCreate) -> NoteGet:
    db_item = await Note(**item.dict()).create(tenant_schema)
    return NoteGet.from_orm(db_item)


@router.get(
    '/get_all',
    status_code=status.HTTP_200_OK,
    summary=f"Create one {model_class.__name__} in the database.",
    description='Endpoint description. Will use the docstring if not provided.',
)
async def get_all(tenant_schema: str) -> List[NoteGet]:
    res = await Note.fetch_all(schema_name = tenant_schema)
    return [NoteGet.from_orm(i) for i in res]
