from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

# Association table for friends
friendship = Table(
    'friendship',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('users.id'), primary_key=True)
)

# Association table for challenge participants
challenge_participants = Table(
    'challenge_participants',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('challenge_id', Integer, ForeignKey('challenges.id'), primary_key=True)
)

class Challenge(Base):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    challenge_type = Column(String(50), nullable=False)  # workout, steps, weight_loss, etc.
    target_value = Column(Integer)  # e.g., number of workouts, steps, or weight loss in grams
    is_public = Column(Boolean, default=True)
    status = Column(String(20), default='active')  # active, completed, cancelled

    # Relationships
    creator = relationship("User", back_populates="created_challenges", foreign_keys=[creator_id])
    participants = relationship("User", secondary=challenge_participants, back_populates="joined_challenges")
    activities = relationship("ChallengeActivity", back_populates="challenge")

class ChallengeActivity(Base):
    __tablename__ = 'challenge_activities'

    id = Column(Integer, primary_key=True)
    challenge_id = Column(Integer, ForeignKey('challenges.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    activity_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    value = Column(Integer, nullable=False)  # e.g., number of steps, workout duration, etc.
    notes = Column(String(200))

    # Relationships
    challenge = relationship("Challenge", back_populates="activities")
    user = relationship("User", back_populates="challenge_activities")

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String(500), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    achievement_id = Column(Integer, ForeignKey('achievements.id'))
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="posts")
    workout = relationship("Workout", back_populates="posts")
    achievement = relationship("Achievement", back_populates="posts")
    likes = relationship("PostLike", back_populates="post")
    comments = relationship("PostComment", back_populates="post")

class PostLike(Base):
    __tablename__ = 'post_likes'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="post_likes")

class PostComment(Base):
    __tablename__ = 'post_comments'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="post_comments")