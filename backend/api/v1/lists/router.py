from fastapi import APIRouter

from api.v1.lists import item, shopping

router = APIRouter()
router.include_router(item.router)
router.include_router(shopping.router)
