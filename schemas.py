# schemas.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    email: Optional[str] = None

# Profile schemas
class UserProfileBase(BaseModel):
    bio: Optional[str] = None
    preferred_language: str = "ASL"
    accessibility_settings: Optional[Dict[str, Any]] = None
    learning_preferences: Optional[Dict[str, Any]] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int
    avatar_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Curriculum schemas
class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    order_index: int
    estimated_duration: Optional[int] = None

class LessonResponse(LessonBase):
    id: int
    module_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ModuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    order_index: int
    difficulty_level: int = 1
    estimated_duration: Optional[int] = None

class ModuleResponse(ModuleBase):
    id: int
    is_active: bool
    created_at: datetime
    lessons: List[LessonResponse] = []
    
    class Config:
        from_attributes = True

# Dictionary schemas
class SignEntryBase(BaseModel):
    word: str
    category: Optional[str] = None
    difficulty: int = 1
    description: Optional[str] = None

class SignEntryResponse(SignEntryBase):
    id: int
    handshapes: Optional[Dict[str, Any]] = None
    movement_pattern: Optional[Dict[str, Any]] = None
    location: Optional[str] = None
    palm_orientation: Optional[str] = None
    facial_expression: Optional[str] = None
    asl_variant: Optional[Dict[str, Any]] = None
    bsl_variant: Optional[Dict[str, Any]] = None
    usage_examples: Optional[List[str]] = None
    video_url: Optional[str] = None
    animation_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Progress schemas
class ProgressBase(BaseModel):
    status: str = "not_started"
    progress_percentage: float = 0.0
    score: Optional[float] = None
    time_spent: Optional[int] = None

class ProgressResponse(ProgressBase):
    id: int
    user_id: int
    module_id: Optional[int] = None
    lesson_id: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_accessed: datetime
    
    class Config:
        from_attributes = True

# Transcription schemas
class TranscriptionRequest(BaseModel):
    session_type: str
    language: str = "ASL"  # ASL or BSL
    settings: Optional[Dict[str, Any]] = None

class TranscriptionResponse(BaseModel):
    session_id: str
    status: str
    confidence: Optional[float] = None
    transcribed_text: Optional[str] = None
    detected_signs: Optional[List[Dict[str, Any]]] = None
    timestamp: datetime

