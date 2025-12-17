# Import all models to ensure SQLAlchemy can resolve relationships
from .user import User
from .models import Workout, WorkoutExercise, WorkoutLog
from .exercise_library import Exercise, Muscle, Equipment, ExerciseProgress
from .achievements import Achievement, UserAchievement
from .gamification import UserStreak, UserPoints
from .social import Challenge, ChallengeActivity, Post, PostComment as Comment, PostLike as Like
from .progress import BodyMeasurement
from .progress_photos import ProgressPhoto
from .workout_planning import WorkoutTemplate, ScheduledWorkout, WorkoutReminder as Reminder
from .progress_tracking import Measurement, PerformanceMetric
from .health_recovery import SleepData, RecoveryMetrics, HealthMetrics, HealthDevice
from .smart_features import AIModel, WorkoutRecommendation, FormCheck, SmartAdjustment