from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    full_name = Column(String)
    
    # Basic relationships
    workouts = relationship("Workout", back_populates="user")
    workout_logs = relationship("WorkoutLog", back_populates="user")
    workout_templates = relationship("WorkoutTemplate", back_populates="user")
    scheduled_workouts = relationship("ScheduledWorkout", back_populates="user")
    
    # Gamification relationships
    achievements = relationship("Achievement", back_populates="user")
    user_achievements = relationship("UserAchievement", back_populates="user")
    streak = relationship("UserStreak", back_populates="user", uselist=False)
    points = relationship("UserPoints", back_populates="user", uselist=False)
    
    # Progress tracking relationships
    body_measurements = relationship("BodyMeasurement", back_populates="user")
    measurements = relationship("Measurement", back_populates="user")
    progress_photos = relationship("ProgressPhoto", back_populates="user")
    custom_exercises = relationship("Exercise", back_populates="creator")
    exercise_progress = relationship("ExerciseProgress", back_populates="user")
    performance_metrics = relationship("PerformanceMetric", back_populates="user")
    
    # Social relationships
    created_challenges = relationship("Challenge", back_populates="creator")
    joined_challenges = relationship("Challenge", secondary="challenge_participants", back_populates="participants")
    challenge_activities = relationship("ChallengeActivity", back_populates="user")
    posts = relationship("Post", back_populates="user")
    post_likes = relationship("PostLike", back_populates="user")
    post_comments = relationship("PostComment", back_populates="user")
    
    # Health and recovery relationships
    sleep_data = relationship("SleepData", back_populates="user")
    recovery_metrics = relationship("RecoveryMetrics", back_populates="user")
    health_metrics = relationship("HealthMetrics", back_populates="user")
    health_devices = relationship("HealthDevice", back_populates="user")
    
    # Smart features relationships
    workout_recommendations = relationship("WorkoutRecommendation", back_populates="user")
    form_checks = relationship("FormCheck", back_populates="user")
    smart_adjustments = relationship("SmartAdjustment", back_populates="user")