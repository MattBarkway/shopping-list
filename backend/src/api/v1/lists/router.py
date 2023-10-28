from fastapi import APIRouter
from src.api.v1.lists import collaborator, item, shopping

router = APIRouter()
router.include_router(item.router)
router.include_router(shopping.router)
router.include_router(collaborator.router)
