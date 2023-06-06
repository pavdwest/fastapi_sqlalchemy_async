from pydantic import BaseModel


class NoteCreate(BaseModel):
    tenant_schema: str
    name: str
    author: str
    release_year: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        schema_extra = {
            'example': {
                'tenant_schema': 'tenant_abcdef',
                'name': 'A Brief Horror Story of Time',
                'author': 'Stephen Hawk King',
                'release_year': 2035,
            }
        }


class NoteGet(BaseModel):
    id: int
    name: str
    author: str
    release_year: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        schema_extra = {
            'example': {
                'id': 27,
                'tenant_schema': 'tenant_abcdef',
                'name': 'A Brief Horror Story of Time',
                'author': 'Stephen Hawk King',
                'release_year': 2035,
            }
        }
