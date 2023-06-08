from __future__ import annotations
from typing import Any, Coroutine
import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy import UUID, select
from sqlalchemy.orm import Mapped, mapped_column
from jose import jwt
from datetime import datetime
from pydantic import ValidationError

from src.logging.service import logger
from src.config import SHARED_SCHEMA_NAME
from src.config import JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth.service import get_hashed_password, reuseable_oauth, ALGORITHM
from src.auth.validators import TokenPayload, TokenCreate
from src.database.service import db

from src.models import AppModel
from src.models import AppModel, SharedModelMixin


class Login(AppModel, SharedModelMixin):
    email:              Mapped[str]         = mapped_column(unique=True, nullable=False)
    password:           Mapped[str]         = mapped_column(nullable=False)
    verification_token: Mapped[uuid.uuid4]  = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    verified:           Mapped[bool]        = mapped_column(nullable=False, default=False)
    name:               Mapped[str]         = mapped_column(nullable=True)
    surname:            Mapped[str]         = mapped_column(nullable=True)

    async def create(self) -> Coroutine[Any, Any, AppModel]:
        self.password = get_hashed_password(self.password)
        await super().create(schema_name=SHARED_SCHEMA_NAME)
        logger.warning(self.verification_token)
        return self


async def get_unverified_login(token: str = Depends(reuseable_oauth)) -> Login:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            # TODO: Auto Renew?
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail='Token expired',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        # Will raise exception if not found. Ensure we always have user's tenant at hand
        # login = await Login.get(email=token_data.sub).prefetch_related('tenant')
        q = select(Login).where(Login.email == token_data.sub).limit(1)
        login = (await db.execute_query(q)).scalar_one_or_none()
        return login

    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

async def get_current_login(token: str = Depends(reuseable_oauth)) -> Login:
    login = await get_unverified_login(token=token)
    if not login.verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Login not verified. Please check email link and verify login first.',
        )
    return login
