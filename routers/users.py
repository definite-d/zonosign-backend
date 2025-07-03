# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserResponse
from auth_utils import verify_token

router = APIRouter()
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token_data = verify_token(credentials.credentials)
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


@router.get(
    "/profile",
    response_model=UserResponse,
    summary="Get current user profile",
    responses={
        200: {"description": "User profile retrieved successfully"},
        401: {"description": "Not authenticated"},
        404: {"description": "User not found"},
    },
)
async def get_profile(current_user: User = Depends(get_current_user)):
    """
    Retrieve the profile of the currently authenticated user.

    Returns a `UserResponse` of the user's profile information including:

    - `id`: User's unique identifier
    - `email`: User's email address
    - `username`: User's chosen username
    - `full_name`: User's full name
    - `created_at`: Account creation timestamp
    - `updated_at`: Last profile update timestamp
    """
    return current_user


@router.put(
    "/profile",
    summary="Update user profile",
    responses={
        200: {"description": "Profile updated successfully"},
        400: {"description": "Invalid profile data"},
        401: {"description": "Not authenticated"},
    },
)
async def update_profile(
    profile_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the profile of the currently authenticated user.

    Takes a dictionary `profile_data` containing profile fields to update. May include:
    - `full_name`: New full name
    - `username`: New username (must be unique)
    - `avatar_url`: URL to user's avatar image

    Returns a success message

    Note: Only the fields provided in the request will be updated.
    Username must be unique across all users.
    """
    # STUB: Implement profile update logic
    return {"message": "Profile updated successfully"}


@router.get(
    "/profile/preferences",
    summary="Get user preferences",
    responses={
        200: {"description": "User preferences retrieved successfully"},
        401: {"description": "Not authenticated"},
    },
)
async def get_preferences(current_user: User = Depends(get_current_user)):
    """
    Retrieve the preferences for the currently authenticated user.

    Returns a dictionary containing the user preferences including:

    - `theme`: UI theme preference (e.g., 'light', 'dark', 'system')
    - `notifications`: Whether notifications are enabled
    - `language`: Preferred language code
    - `accessibility`: Accessibility settings
    - `email_notifications`: Email notification preferences
    """
    # STUB: Return user preferences
    return {"preferences": {"theme": "dark", "notifications": True}}


@router.put(
    "/profile/preferences",
    summary="Update user preferences",
    responses={
        200: {"description": "Preferences updated successfully"},
        400: {"description": "Invalid preferences data"},
        401: {"description": "Not authenticated"},
    },
)
async def update_preferences(
    preferences: dict, current_user: User = Depends(get_current_user)
):
    """
    Update the preferences for the currently authenticated user.

    Takes a dictionary `preferences` containing preference fields to update.
    May include any user preference key-value pairs.

    Returns a success message

    Note: Only the preference fields provided in the request will be updated.
    Unrecognized preference keys will be ignored.
    """
    # STUB: Implement preferences update
    return {"message": "Preferences updated successfully"}
