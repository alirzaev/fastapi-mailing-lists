import logging
from typing import Dict, Any

import emails

from application import schemas, crud
from application.core.config import config
from application.database.session import AsyncSessionLocal


def send_email(
        email_to: str,
        subject: str = '',
        content: str = '',
        environment: Dict[str, Any] = {},  # noqa
) -> None:
    assert config.EMAILS_ENABLED, 'no provided configuration for email variables'
    message = emails.Message(
        mail_from=('Project', 'info@example.com'),
        subject=subject,
        html=content,
    )
    smtp_options = dict(host=config.SMTP_HOST, port=config.SMTP_PORT)
    if config.SMTP_TLS:
        smtp_options['tls'] = True
    if config.SMTP_USER:
        smtp_options['user'] = config.SMTP_USER
    if config.SMTP_PASSWORD:
        smtp_options['password'] = config.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f'send email result: {response}')


async def send_email_to_mailing_list(email_content: schemas.EmailContent):
    async with AsyncSessionLocal() as db:
        mailing_list = await crud.subscription_email.get_all(db)

        for subscription in mailing_list:
            send_email(subscription.email, email_content.subject, email_content.content)
