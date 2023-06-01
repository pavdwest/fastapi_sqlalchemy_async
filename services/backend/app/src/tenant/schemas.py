from uuid import UUID

from pydantic import BaseModel


class TenantCreate(BaseModel):
    identifier: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        schema_extra = {
            'example': {
                'identifier': 'BlueMigrant',
            }
        }


class TenantGet(BaseModel):
    id: int
    identifier: str
    schema_name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        schema_extra = {
            'example': {
                'id': 27,
                'schema_name': 'f0e7207e-5568-45ff-b877-74eb658649de',
                'identifier': 'BlueMigrant',
            }
        }
