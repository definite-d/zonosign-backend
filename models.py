# models.py
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user_progress = relationship("UserProgress", back_populates="user")
    practice_sessions = relationship("PracticeSession", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    avatar_url = Column(String)
    bio = Column(Text)
    preferred_language = Column(String, default="ASL")  # ASL or BSL
    accessibility_settings = Column(JSON)
    learning_preferences = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Module(Base):
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    order_index = Column(Integer, nullable=False)
    difficulty_level = Column(Integer, default=1)
    estimated_duration = Column(Integer)  # minutes
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lessons = relationship("Lesson", back_populates="module")

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    content = Column(JSON)  # Lesson content structure
    order_index = Column(Integer, nullable=False)
    estimated_duration = Column(Integer)  # minutes
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    module = relationship("Module", back_populates="lessons")

class SignEntry(Base):
    __tablename__ = "sign_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, nullable=False, index=True)
    category = Column(String, index=True)
    difficulty = Column(Integer, default=1)
    description = Column(Text)
    handshapes = Column(JSON)  # Handshape sequence data
    movement_pattern = Column(JSON)  # Movement data
    location = Column(String)  # Body location
    palm_orientation = Column(String)
    facial_expression = Column(String)
    asl_variant = Column(JSON)  # ASL-specific data
    bsl_variant = Column(JSON)  # BSL-specific data
    usage_examples = Column(JSON)  # Example sentences
    video_url = Column(String)
    animation_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    module_id = Column(Integer, ForeignKey("modules.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    status = Column(String, default="not_started")  # not_started, in_progress, completed
    progress_percentage = Column(Float, default=0.0)
    score = Column(Float)
    time_spent = Column(Integer)  # minutes
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="user_progress")

class PracticeSession(Base):
    __tablename__ = "practice_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_type = Column(String, nullable=False)  # transcription, practice, assessment
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    duration = Column(Integer)  # seconds
    accuracy_score = Column(Float)
    session_data = Column(JSON)  # Session-specific data
    
    # Relationships
    user = relationship("User", back_populates="practice_sessions")

