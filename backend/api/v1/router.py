"""Defines routing for API endpoints."""
from fastapi import APIRouter

from api.v1.shopping import shopping
from api.v1.user import collaborator, auth

router = APIRouter()

# shopping.router.include_router(router=item.router, tags=["Item"], prefix="/item")

router.include_router(router=auth.router, tags=["Auth"], prefix="/auth")
router.include_router(router=shopping.router, tags=["Shopping"], prefix="/shopping")
router.include_router(
    router=collaborator.router, tags=["Collaborator"], prefix="/collaborator"
)
