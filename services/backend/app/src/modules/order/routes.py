from typing import List, Dict

from fastapi import APIRouter, status, HTTPException
from fastapi import status
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from inflection import pluralize

from src.database.service import db
from src.modules.order.models import Order
from src.modules.order.validators import OrderCreate, OrderGet


Model = Order
GetModelValidator = OrderGet
CreateModelValidator = OrderCreate


router = APIRouter(
    tags=[Model.__tablename_friendly__],
    prefix=f"/{Model.__tablename__}",
)


@router.post(
    f"/create_one",
    status_code=status.HTTP_200_OK,
    summary=f"Create one {Model.__name__} in the database.",
    description='Endpoint description. Will use the docstring if not provided.',
)
async def create_one(tenant_schema: str, item: CreateModelValidator) -> GetModelValidator:
    try:
        db_item = await Model(**item.dict()).create(tenant_schema)
        return GetModelValidator.from_orm(db_item)
    except IntegrityError as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ex.args,
        )


@router.get(
    '/get_all',
    status_code=status.HTTP_200_OK,
    summary=f"Get all {pluralize(Model.__name__)} from the database.",
    description='Endpoint description. Will use the docstring if not provided.',
)
async def get_all(tenant_schema: str) -> List[GetModelValidator]:
    res = await Model.fetch_all(schema_name = tenant_schema)
    print(res[0].__dict__)
    print(res[0].guid)
    return [GetModelValidator.from_orm(i) for i in res]
