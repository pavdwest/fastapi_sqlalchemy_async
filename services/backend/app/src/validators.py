from typing import Union

from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid


class IdValidator(BaseModel):
    id: int


class TimestampValidator(BaseModel):
    timestamp: datetime


class TimestampsValidator(BaseModel):
    created_at: datetime
    updated_at: datetime


class IdentifierValidator(BaseModel):
    identifier: str


class DescriptionValidator(BaseModel):
    description: str


class GUIDValidator(BaseModel):
    guid: uuid.UUID


class AppModelGetValidator(IdValidator, TimestampsValidator):
    class Config:
        from_attributes = True
        populate_by_name = True

class AppModelCreateValidator(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True
