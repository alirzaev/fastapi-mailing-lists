from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from application.database.models import SubscriptionEmail
from application.schemas import SubscriptionEmailCreate


async def create(db: AsyncSession, subscription_email_in: SubscriptionEmailCreate) -> SubscriptionEmail:
    subscription_email = SubscriptionEmail(email=subscription_email_in.email)

    db.add(subscription_email)
    await db.commit()
    await db.refresh(subscription_email)

    return subscription_email


async def get_by_email(db: AsyncSession, email: str) -> Optional[SubscriptionEmail]:
    result = await db.execute(select(SubscriptionEmail).filter(SubscriptionEmail.email == email))
    return result.scalars().first()


async def get_all(db: AsyncSession) -> List[SubscriptionEmail]:
    result = await db.execute(select(SubscriptionEmail))
    return result.scalars()


async def remove(db: AsyncSession, email: str) -> Optional[SubscriptionEmail]:
    subscription_email = await get_by_email(db, email)

    if subscription_email is not None:
        await db.delete(subscription_email)
        await db.commit()

    return subscription_email
