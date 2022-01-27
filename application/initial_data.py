import asyncio
import logging

from application.database.init_db import init_db
from application.database.session import AsyncSessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    async with AsyncSessionLocal() as db:
        await init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    asyncio.run(init())
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
