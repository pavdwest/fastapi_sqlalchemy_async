from datetime import datetime

from pydantic import BaseModel

from src.validators import (
    AppModelGetValidator,
    AppModelCreateValidator,
    TimestampValidator,
    DescriptionValidator,
    GUIDValidator,
)


class OrderCommon(BaseModel):
    product_id: int
    client: str
    quantity: int
    unit_price: float
    amount: float


class OrderCreate(AppModelCreateValidator, TimestampValidator, DescriptionValidator, OrderCommon):
    class Config:
        from_attributes = True
        populate_by_name = True

        json_schema_extra = {
            'example': {
                'timestamp': datetime.now(),
                'description': 'Some order for a client - URGENT!',
                'product_id': 27,
                'client': 'client@incrediblecorruption.com',
                'quantity': 5,
                'unit_price': 4.25,
                'amount': 21.25,
            }
        }


class OrderGet(AppModelGetValidator, TimestampValidator, DescriptionValidator, GUIDValidator, OrderCommon):
    class Config:
        from_attributes = True
        populate_by_name = True

        json_schema_extra = {
            'example': {
                'id': 27,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'timestamp': datetime.now(),
                'description': 'Some order for a client - not urgent at all.',
                'guid': '3189f658-f3ba-49a4-a66b-cb9219b4d603',
                'product_id': 27,
                'client': 'client@incrediblecorruption.com',
                'quantity': 5,
                'unit_price': 4.25,
                'amount': 21.25,
            }
        }
