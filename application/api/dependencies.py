from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # noqa
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from application import crud
from application.core import security
from application.core.config import config
from application.database.models import User
from application.database.redis_client import redis_client
from application.database.session import AsyncSessionLocal
from application.schemas import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl='/auth/signin')


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


async def get_token_payload(
        token: str = Depends(reusable_oauth2)
) -> TokenPayload:
    try:
        decoded = jwt.decode(token, config.SECRET_KEY, algorithms=security.ALGORITHM)
        payload = TokenPayload(**decoded)

        entry = await redis_client.get(payload.jwti)
        if entry:
            raise HTTPException(
                status_code=403,
                detail='The token was revoked'
            )

        return payload
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail='Could not validate credentials'
        )


async def get_current_user(
        db: AsyncSession = Depends(get_db), token_payload: TokenPayload = Depends(get_token_payload)
) -> User:
    user = await crud.user.get(db, token_payload.sub)

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return user
