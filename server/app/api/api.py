from fastapi import APIRouter
from app.api.endpoints import (
    users,
    workouts,
    nutrition,
    social,
    health,
    scheduling,
    smart_scheduling
)

api_router = APIRouter()

# Include all API endpoints
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(workouts.router, prefix="/workouts", tags=["workouts"])
api_router.include_router(nutrition.router, prefix="/nutrition", tags=["nutrition"])
api_router.include_router(social.router, prefix="/social", tags=["social"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(scheduling.router, prefix="/scheduling", tags=["scheduling"])
api_router.include_router(
    smart_scheduling.router,
    prefix="/smart-scheduling",
    tags=["smart-scheduling"]
)