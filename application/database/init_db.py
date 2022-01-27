from application.database import base  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession

from application import crud, schemas
from application.core.config import config


# make sure all SQL Alchemy models are imported (application.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


async def init_db(db: AsyncSession) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = await crud.user.get_by_email(db, email=config.FIRST_SUPERUSER)

    if not user:
        user_in = schemas.UserCreate(
            email=config.FIRST_SUPERUSER,
            password=config.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        await crud.user.create(db, user_in)
