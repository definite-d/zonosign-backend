# routers/progress.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import UserProgress, User
from schemas import ProgressResponse
from routers.users import get_current_user

router = APIRouter()


@router.get(
    "/overview",
    summary="Get overall learning progress",
    responses={
        200: {"description": "Progress overview retrieved successfully"},
        401: {"description": "Not authenticated"},
    },
)
async def get_progress_overview(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Retrieve an overview of the user's learning progress.

    Returns a summary including:
    - `Total` number of modules in the curriculum
    - `Number` of completed modules
    - `Current` module the user is working on
    - `Overall` progress percentage
    - `Total` time spent learning (in minutes)

    This provides a high-level view of the user's learning journey.
    """
    # STUB: Calculate and return progress overview
    return {
        "total_modules": 12,
        "completed_modules": 3,
        "current_module": 4,
        "overall_progress": 25.0,
        "time_spent_total": 1250,  # minutes
    }


@router.get(
    "/modules",
    response_model=List[ProgressResponse],
    summary="Get detailed module progress",
    responses={
        200: {"description": "Module progress retrieved successfully"},
        401: {"description": "Not authenticated"},
    },
)
async def get_module_progress(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Retrieve detailed progress for all modules.

    Returns a list containing progress information for each module:
    - `Module` ID and name
    - `Completion` status
    - `Score`/grade (if applicable)
    - `Time` spent
    - `Last` accessed timestamp

    This provides granular progress tracking per module.
    """
    progress = (
        db.query(UserProgress).filter(UserProgress.user_id == current_user.id).all()
    )
    return progress


@router.post(
    "/lessons/{lesson_id}/start",
    status_code=201,
    summary="Start a lesson",
    responses={
        201: {"description": "Lesson started successfully"},
        400: {"description": "Lesson already in progress"},
        401: {"description": "Not authenticated"},
        404: {"description": "Lesson not found"},
    },
)
async def start_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Mark a lesson as started for the current user.

    - `lesson_id`: The ID of the lesson to start

    Records the start time of the lesson and creates a progress record.
    Returns a success message with the lesson ID.

    Note: Only one lesson can be in progress at a time per user.
    """
    # STUB: Implement lesson start logic
    # 1. Verify lesson exists and is accessible
    # 2. Check no other lesson is in progress
    # 3. Create/update progress record with start time
    return {"message": "Lesson started", "lesson_id": lesson_id}


@router.post(
    "/lessons/{lesson_id}/complete",
    summary="Complete a lesson",
    responses={
        200: {"description": "Lesson completed successfully"},
        400: {"description": "Lesson not started or already completed"},
        401: {"description": "Not authenticated"},
        404: {"description": "Lesson not found"},
    },
)
async def complete_lesson(
    lesson_id: int,
    score: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Mark a lesson as completed and record the score.

    - `lesson_id`: The ID of the lesson to complete
    - `score`: The score achieved (0.0 to 1.0)

    Updates the progress record with completion status, score, and end time.
    Calculates time spent based on start time.

    Returns the completion status and recorded score.
    """
    # STUB: Implement lesson completion logic
    # 1. Verify lesson exists and is accessible
    # 2. Check lesson is in progress for this user
    # 3. Update progress record with completion status and score
    # 4. Calculate time spent and update user's total learning time
    return {"message": "Lesson completed", "lesson_id": lesson_id, "score": score}
