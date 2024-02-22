from app.api.api_v1.routers import roles, user_roles, users
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(roles.router)
api_router.include_router(user_roles.router)
