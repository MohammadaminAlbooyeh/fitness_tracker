from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.models import models
from app.models.user import User
from app.routes import auth, workouts, exercise_library, workout_planning, gamification, progress_tracking, social
from app.api.endpoints import smart_features, health_recovery

# Create database tables
engine.connect()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Tracker API")

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(workouts.router, prefix="/api/workouts", tags=["Workouts"])
app.include_router(exercise_library.router, prefix="/api", tags=["Exercises"])
app.include_router(workout_planning.router, prefix="/api/workouts", tags=["Workout Planning"])
app.include_router(gamification.router, prefix="/api", tags=["Gamification"])
app.include_router(progress_tracking.router, prefix="/api", tags=["Progress Tracking"])
app.include_router(social.router, prefix="/api", tags=["Social"])
app.include_router(smart_features.router, prefix="/api/smart", tags=["Smart Features"])
app.include_router(health_recovery.router, prefix="/api/health", tags=["Health and Recovery"])

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Fitness Tracker API"}