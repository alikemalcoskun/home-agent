from fastapi import APIRouter
from app.api.v1.router import router as v1_router
from app.api.v2.router import router as v2_router

router = APIRouter()

router.include_router(v1_router, prefix="/v1")
router.include_router(v2_router, prefix="/v2")
