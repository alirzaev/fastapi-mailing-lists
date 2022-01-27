from typing import Optional, Dict, Any

from pydantic import BaseSettings, validator, EmailStr


class Config(BaseSettings):
    DEBUG: bool = True

    SQLALCHEMY_DATABASE_URL: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'

    REDIS_URL: str = 'redis://localhost/0'

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    SECRET_KEY: str = 'very_secret_key'

    SMTP_TLS: bool = True

    SMTP_PORT: Optional[int] = None

    SMTP_HOST: Optional[str] = None

    SMTP_USER: Optional[str] = None

    SMTP_PASSWORD: Optional[str] = None

    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:  # noqa
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
        )

    FIRST_SUPERUSER: EmailStr = 'admin@example.com'

    FIRST_SUPERUSER_PASSWORD: str = 'password'


config = Config()
