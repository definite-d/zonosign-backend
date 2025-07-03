# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from models import User, UserProfile
from schemas import UserCreate, UserLogin, UserResponse, Token
from auth_utils import verify_password, get_password_hash, create_access_token
from setttings import settings

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Email already registered or username taken"},
    },
)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with the provided information.

    - `email`: Must be a valid email address and not already registered
    - `username`: Must be unique
    - `password`: Will be hashed before storage
    - `full_name`: User's full name

    Returns the created user object without sensitive information.
    """
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Check username
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # Create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create user profile
    user_profile = UserProfile(user_id=db_user.id)
    db.add(user_profile)
    db.commit()

    return db_user


@router.post(
    "/login",
    response_model=Token,
    summary="User login",
    responses={
        200: {"description": "Login successful, token returned"},
        401: {"description": "Incorrect email or password"},
    },
)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and return an access token.

    - `email`: User's registered email
    - `password`: User's password

    Returns an access token that should be included in the Authorization header
    for protected endpoints.
    """
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.post(
    "/logout",
    summary="User logout",
    responses={200: {"description": "Logout successful"}},
)
async def logout():
    """
    Log out the current user.

    Note: In production, this should invalidate the current access token.
    Currently, this is a stub implementation.
    """
    # STUB: In production, implement token blacklisting
    return {"message": "Logout successful"}


@router.post(
    "/forgot-password",
    summary="Request password reset",
    responses={200: {"description": "Password reset email sent if the email exists"}},
)
async def forgot_password(email: str):
    """
    Initiate password reset process.

    - `email`: The email address to send the reset link to

    Note: This is a stub implementation. In production, this would send
    an email with a password reset link.
    """
    # STUB: Implement email sending for password reset
    return {"message": "Password reset email sent"}


@router.post(
    "/reset-password",
    summary="Reset password with token",
    responses={
        200: {"description": "Password reset successful"},
        400: {"description": "Invalid or expired token"},
    },
)
async def reset_password(token: str, new_password: str):
    """
    Reset user's password using a valid reset token.

    - `token`: The reset token received via email
    - `new_password`: The new password to set

    Note: This is a stub implementation. In production, this would validate
    the token and update the user's password.
    """
    # STUB: Implement password reset with token validation
    return {"message": "Password reset successful"}
