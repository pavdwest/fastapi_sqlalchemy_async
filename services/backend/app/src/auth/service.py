from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any, Dict
from uuid import uuid4, UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from src.config import JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth.validators import TokenPayload, TokenCreate
from src.login.models import Login


ALGORITHM = 'HS256'


password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def bearer_token_header(token: str) -> Dict:
    return {
        'Authorization': f"Bearer {token}"
    }

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def get_random_token() -> UUID:
    """
    Utility method for random token.
    Not related to authentication flow really.

    Returns:
        str: Random token string
    """
    return uuid4()


def encode_item(item: Dict) -> str:
    """
    Encodes item in JWT

    Returns:
        str: Encoded JWT
    """
    return jwt.encode(item, JWT_SECRET_KEY, ALGORITHM)


def create_access_token(subject: Union[str, Any], expire_minutes: float = None) -> str:
    """
    Create access token for the Login.

    Args:
        subject (Union[str, Any]): Login data e.g. email address
        expire_minutes (float, optional): How long before token expires. Defaults ACCESS_TOKEN_EXPIRE_MINUTES if not provided.

    Returns:
        str: valid token
    """
    if expire_minutes is None:
        expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES

    token_expires = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode = TokenCreate(
        sub=str(subject),
        exp=token_expires
    )
    encoded_jwt = encode_item(to_encode.dict())
    return encoded_jwt


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/get_access_token",
    scheme_name="JWT"
)


# async def get_unverified_login(token: str = Depends(reuseable_oauth)) -> Login:
#     """
#     Retrieves a Login stored in the database from the provided token data.
#     Does not care whether the Login is verified or not.
#     Do not use for protected routes except for very specific cases!

#     Args:
#         token (str, optional): Encoded token. Defaults to Depends(reuseable_oauth).

#     Raises:
#         HTTPException: 401 if the token has expired
#         HTTPException: 403 if credentials are invalid

#     Returns:
#         Login: Login record from the db
#     """
#     try:
#         payload = jwt.decode(
#             token,
#             JWT_SECRET_KEY,
#             algorithms=[ALGORITHM]
#         )
#         token_data = TokenPayload(**payload)

#         if datetime.fromtimestamp(token_data.exp) < datetime.now():
#             # TODO: Auto Renew?
#             raise HTTPException(
#                 status_code = status.HTTP_401_UNAUTHORIZED,
#                 detail='Token expired',
#                 headers={'WWW-Authenticate': 'Bearer'},
#             )

#     except(jwt.JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail='Could not validate credentials',
#             headers={'WWW-Authenticate': 'Bearer'},
#         )

#     # Will raise exception if not found. Ensure we always have user's tenant at hand
#     login = await Login.get(email=token_data.sub).prefetch_related('tenant')

#     return login


# async def get_current_login(token: str = Depends(reuseable_oauth)) -> Login:
#     """
#     Retrieves a Login stored in the database from the provided token data.
#     Will raise an exception if the Login has not been verified yet.
#     Use this for all protected routes except in very specific cases.

#     Args:
#         token (str, optional): Encoded token. Defaults to Depends(reuseable_oauth).

#     Raises:
#         HTTPException: 403 if Login not verified

#     Returns:
#         Login: Login record from the db
#     """
#     login = await get_unverified_login(token=token)

#     if not login.verified:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail='Login not verified. Please check email link and verify login first.',
#         )

#     return login
