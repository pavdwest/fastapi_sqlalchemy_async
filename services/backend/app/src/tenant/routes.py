from typing import List

from fastapi import APIRouter, status

from src.database.service import db
from src.tenant.models import Tenant
from src.tenant.schemas import TenantCreate, TenantGet


model_class = Tenant


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
async def create_one(item: TenantCreate) -> TenantGet:
    tenant = await Tenant(**item.dict()).create()
    await tenant.provision()
    return TenantGet.from_orm(tenant)
