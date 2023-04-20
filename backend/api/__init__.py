from fastapi import APIRouter
from . import recipes, auth, users

router = APIRouter(
    prefix='/api'
)
router.include_router(recipes.router)
router.include_router(auth.router)
router.include_router(users.router)