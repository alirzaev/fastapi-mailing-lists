from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from application.core.security import get_password_hash, verify_password
from application.database.models import User
from application.schemas import UserCreate


async def create(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        name=user_in.name,
        hashed_password=get_password_hash(user_in.password)
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get(db: AsyncSession, id: int) -> Optional[User]:  # noqa
    result = await db.execute(select(User).filter(User.id == id))
    return result.scalars().first()


async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def authenticate(db: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await get_by_email(db, email)

    if user is None:
        return None
    elif not verify_password(password, user.hashed_password):
        return None
    else:
        return user
