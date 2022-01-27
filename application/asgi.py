import uvicorn
from fastapi import FastAPI

from application.api.routers import api_router
from application.core.config import config

application = FastAPI(
    debug=config.DEBUG,
    title='Mailing lists service',
    description='A service for mailing lists'
)
application.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(application, port=8000, debug=config.DEBUG)  # noqa