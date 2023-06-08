from datetime import datetime
import uuid

from pydantic import BaseModel

from src.validators import (
    AppModelGetValidator,
    AppModelCreateValidator,
)


class LoginCommon(BaseModel):
    email:         str
    name:          str = None
    surname:       str = None


class LoginCreate(AppModelCreateValidator, LoginCommon):
    password: str
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        schema_extra = {
            'example': {
                'email': 'joe.doe@incrediblecorruption.com',
                'password': '5up3rS3<uR3',
                'name': 'Joe',
                'surname': 'Doe',
            }
        }


class LoginGet(AppModelGetValidator, LoginCommon):
    # verification_token: uuid.UUID     # Send via email instead
    verified: bool
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
