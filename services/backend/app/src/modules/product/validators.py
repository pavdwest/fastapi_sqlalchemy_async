from pydantic import BaseModel


class ProductCreate(BaseModel):
    identifier: str
    description: str
    release_year: int

    class Config:
        from_attributes = True
        populate_by_name = True

        json_schema_extra = {
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
        from_attributes = True
        populate_by_name = True

        json_schema_extra = {
            'example': {
                'id': 27,
                'identifier': 'Retro Encabulator',
                'description': 'An encabulator that is retro',
                'release_year': 2005,
            }
        }
