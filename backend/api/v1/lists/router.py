from api.v1.lists import collaborator, item, shopping
from fastapi import APIRouter

router = APIRouter()
router.include_router(item.router)
router.include_router(shopping.router)
router.include_router(collaborator.router)
