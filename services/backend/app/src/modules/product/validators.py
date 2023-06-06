from pydantic import BaseModel


class ProductCreate(BaseModel):
    identifier: str
    description: str
    release_year: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        schema_extra = {
            'example': {
                'identifier': 'Retro Encabulator',
                'description': 'An encabulator that is retro',
                'release_year': 2005,
            }
        }


class ProductGet(BaseModel):
    id: int
    identifier: str
    description: str
    release_year: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        schema_extra = {
            'example': {
                'id': 27,
                'identifier': 'Retro Encabulator',
                'description': 'An encabulator that is retro',
                'release_year': 2005,
            }
        }
