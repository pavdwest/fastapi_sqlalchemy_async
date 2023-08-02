from pydantic import BaseModel


class NoteCreate(BaseModel):
    name: str
    author: str
    release_year: int

    class Config:
        from_attributes = True
        populate_by_name = True

        json_schema_extra = {
            'example': {
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
        from_attributes = True
        populate_by_name = True

        json_schema_extra = {
            'example': {
                'id': 27,
                'name': 'A Brief Horror Story of Time',
                'author': 'Stephen Hawk King',
                'release_year': 2035,
            }
        }
