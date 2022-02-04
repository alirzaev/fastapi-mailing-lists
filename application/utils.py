import logging
from pathlib import Path
from typing import Dict, Any

import emails
from emails.template import JinjaTemplate

from application import schemas, crud
from application.core.config import config
from application.core.security import create_unsubscribe_token
from application.database.session import AsyncSessionLocal

_TEMPLATES_DIR = Path(__file__).parent / 'templates'


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


def render_template(template_name, **context):
    template_str = (_TEMPLATES_DIR / template_name).read_text()

    return JinjaTemplate(template_str).render(**context)


async def send_email_to_mailing_list(email_content: schemas.EmailContent):
    async with AsyncSessionLocal() as db:
        mailing_list = await crud.subscription_email.get_all(db)

        path = _TEMPLATES_DIR / 'email' / 'mailing_list_email.html'
        template = JinjaTemplate(path.read_text())

        for subscription in mailing_list:
            token = create_unsubscribe_token(subscription.email)
            content = template.render(
                content=email_content.content,
                unsubscribe_link=f'{config.SERVER_HOST}/mailing/unsubscribe/{token}'
            )
            send_email(subscription.email, email_content.subject, content)
