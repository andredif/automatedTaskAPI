from fastapi import APIRouter
from . import auth, tasks


router = APIRouter(
    prefix="/api/v1"
)

router.include_router(auth.router)
router.include_router(tasks.router)