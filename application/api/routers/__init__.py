from fastapi import APIRouter

from .auth import router as auth_router
from .mailing import router as mailing_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix='/auth')
api_router.include_router(mailing_router, prefix='/mailing')
