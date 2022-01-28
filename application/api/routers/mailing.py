from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from application import crud
from application import schemas
from application.api.dependencies import get_db

router = APIRouter(tags=['mailing'])


@router.post('/subscribe', response_model=schemas.SubscriptionEmail)
async def subscribe(
        subscription_email_in: schemas.SubscriptionEmailCreate,
        db: AsyncSession = Depends(get_db)
):
    subscription_email = await crud.subscription_email.get_by_email(db, subscription_email_in.email)

    if subscription_email is not None:
        raise HTTPException(
            status_code=400,
            detail='This email already exists in the mailing list.'
        )
    subscription_email = await crud.subscription_email.create(db, subscription_email_in)

    return subscription_email
