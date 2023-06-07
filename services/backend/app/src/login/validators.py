from datetime import datetime

from pydantic import BaseModel

from src.validators import (
    AppModelGetValidator,
    AppModelCreateValidator,
    TimestampValidator,
    DescriptionValidator,
    GUIDValidator,
)


class LoginCommon(BaseModel):
    email:         str
    password_hash: str
    verified:      bool
    name:          str
    surname:       str


class LoginCreate(AppModelCreateValidator, TimestampValidator, DescriptionValidator, LoginCommon):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        schema_extra = {
            'example': {
                'email': 'joe.doe@incrediblecorruption.com',
                'verified': True,
                'name': 'Joe',
                'surname': 'Doe',
            }
        }


class LoginGet(AppModelGetValidator, TimestampValidator, DescriptionValidator, GUIDValidator, LoginCommon):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        schema_extra = {
            'example': {
                'id': 27,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'email': 'joe.doe@incrediblecorruption.com',
                'verified': True,
                'name': 'Joe',
                'surname': 'Doe',
            }
        }
