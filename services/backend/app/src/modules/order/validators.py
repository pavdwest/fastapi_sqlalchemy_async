from datetime import datetime

from src.validators import (
    AppModelGetValidator,
    AppModelCreateValidator,
    TimestampValidator,
    DescriptionValidator,
    GUIDValidator,
)


class OrderCreate(AppModelCreateValidator, TimestampValidator, DescriptionValidator):
    product_id: int
    client: str
    quantity: int
    unit_price: float
    amount: float

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        schema_extra = {
            'example': {
                'timestamp': datetime.now(),
                'description': 'Some order for a client - URGENT!',
                'product_id': 27,
                'client': 'client1@incrediblecorruption.com',
                'quantity': 5,
                'unit_price': 4.25,
                'amount': 21.25,
            }
        }


class OrderGet(AppModelGetValidator, TimestampValidator, DescriptionValidator, GUIDValidator):
    product_id: int
    client: str
    quantity: int
    unit_price: float
    amount: float

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        schema_extra = {
            'example': {
                'id': 27,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'timestamp': datetime.now(),
                'description': 'Some order for a client - URGENT!',
                'guid': '3189f658-f3ba-49a4-a66b-cb9219b4d603',
                'product_id': 27,
                'client': 'client1@incrediblecorruption.com',
                'quantity': 5,
                'unit_price': 4.25,
                'amount': 21.25,
            }
        }
