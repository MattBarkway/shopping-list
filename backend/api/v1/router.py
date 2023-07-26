"""Defines routing for API endpoints."""
from fastapi import APIRouter

from api.v1 import auth, shopping, item, collaborator

router = APIRouter()

router.include_router(router=auth.router, tags=["Auth"], prefix="/auth")
router.include_router(router=shopping.router, tags=["Shopping"], prefix="/shopping")
router.include_router(router=item.router, tags=["Item"], prefix="/item")
router.include_router(
    router=collaborator.router, tags=["Collaborator"], prefix="/collaborator"
)
