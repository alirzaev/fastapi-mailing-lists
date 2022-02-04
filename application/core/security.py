from datetime import datetime, timedelta
from secrets import token_hex
from typing import Any, Union, Optional

from jose import jwt  # noqa
from passlib.context import CryptContext
from pydantic import ValidationError

from application.core.config import config

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

ALGORITHM = 'HS256'


def create_access_token(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {'exp': expire, 'sub': str(subject), 'jwti': token_hex(32)}
    encoded = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)

    return encoded


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_unsubscribe_token(email: str) -> str:
    to_encode = {'sub': email}
    encoded = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)

    return encoded


def decode_unsubscribe_token(token: str) -> Optional[str]:
    try:
        decoded = jwt.decode(token, config.SECRET_KEY, algorithms=ALGORITHM)
        return decoded['sub']
    except (jwt.JWTError, ValidationError):
        return None
