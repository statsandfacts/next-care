from app.api.api_v1.routers import cases, roles, user_roles, users, level_value_mapping, master_questionnaire, records
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(roles.router)
api_router.include_router(user_roles.router)
api_router.include_router(cases.router)
api_router.include_router(level_value_mapping.router)
api_router.include_router(master_questionnaire.router)
api_router.include_router(records.router)
