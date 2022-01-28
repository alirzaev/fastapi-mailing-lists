from typing import Optional

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
