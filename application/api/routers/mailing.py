from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from application import crud
from application import schemas
from application.api.dependencies import get_db, get_current_user
from application.core.security import decode_unsubscribe_token
from application.database.models import User
from application.utils import send_email_to_mailing_list, render_template

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


@router.post('/sendEmail', status_code=204)
async def send_email(
        background_tasks: BackgroundTasks,
        email_content: schemas.EmailContent,
        _: User = Depends(get_current_user)
):
    background_tasks.add_task(send_email_to_mailing_list, email_content)
    return Response(status_code=204)


@router.get('/unsubscribe/{token}', status_code=200, response_class=HTMLResponse)
async def unsubscribe(
        token: str = Path(...),
        db: AsyncSession = Depends(get_db)
):
    email = decode_unsubscribe_token(token)

    if email is not None:
        await crud.subscription_email.remove(db, email)
        return render_template('unsubscribed.html',
                               title='Unsubscribed',
                               message='You have been successfully unsubscribed from the mailing list')
    else:
        return render_template('unsubscribed.html',
                               title='Something went wrong',
                               message='Failed to unsubscribe')
