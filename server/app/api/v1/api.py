from fastapi import APIRouter
from app.api.v1.endpoints import (
    users,
    auth,
    profiles,
    workouts,
    exercises,
    nutrition,
    tracking,
    goals,
    professionals,
    consultations,
    payments
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(workouts.router, prefix="/workouts", tags=["workouts"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
api_router.include_router(nutrition.router, prefix="/nutrition", tags=["nutrition"])
api_router.include_router(tracking.router, prefix="/tracking", tags=["tracking"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(
    professionals.router,
    prefix="/professionals",
    tags=["professionals"]
)
api_router.include_router(
    consultations.router,
    prefix="/consultations",
    tags=["consultations"]
)
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])