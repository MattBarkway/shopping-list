"""Defines routing for API endpoints."""
from fastapi import APIRouter

from api.v1.lists import router as lists_router
from api.v1 import auth, collaborator

router = APIRouter()

router.include_router(router=lists_router.router, tags=["Shopping"], prefix="/shopping")
router.include_router(router=auth.router, tags=["Auth"], prefix="/auth")
router.include_router(
    router=collaborator.router, tags=["Collaborator"], prefix="/collaborator"
)
