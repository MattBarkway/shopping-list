"""Defines routing for API endpoints."""
from api.v1 import auth
from api.v1.lists import collaborator
from api.v1.lists import router as lists
from fastapi import APIRouter

router = APIRouter()

router.include_router(router=lists.router, tags=["Shopping"], prefix="/shopping")
router.include_router(router=auth.router, tags=["Auth"], prefix="/auth")
router.include_router(
    router=collaborator.router, tags=["Collaborator"], prefix="/collaborator"
)
