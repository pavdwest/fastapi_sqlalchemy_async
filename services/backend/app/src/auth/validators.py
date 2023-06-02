from datetime import datetime

from pydantic import BaseModel


class TokenGet(BaseModel):
    access_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class TokenCreate(BaseModel):
    sub: str = None
    exp: datetime = None
