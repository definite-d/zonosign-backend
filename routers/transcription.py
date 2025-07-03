# routers/transcription.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from database import get_db
from models import PracticeSession, User
from schemas import TranscriptionRequest
from routers.users import get_current_user
from datetime import datetime

from setttings import settings

router = APIRouter()


@router.post(
    "/start-session",
    summary="Start a new transcription session",
    responses={
        200: {"description": "Session started successfully"},
        401: {"description": "Not authenticated"},
    },
)
async def start_transcription_session(
    request: TranscriptionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Initialize a new sign language transcription session.

    - `language`: The target sign language for transcription (e.g., 'ASL', 'BSL')
    - `settings`: Additional configuration for the transcription session

    Returns a session ID that should be used for subsequent frame submissions.
    """
    # Create practice session
    session = PracticeSession(
        user_id=current_user.id,
        session_type="transcription",
        session_data={"language": request.language, "settings": request.settings},
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "session_id": str(session.id),
        "status": "started",
        "language": request.language,
    }


@router.post(
    "/process-frame",
    summary="Process a single video frame",
    responses={
        200: {"description": "Frame processed successfully"},
        400: {"description": "Invalid session ID or frame data"},
        401: {"description": "Not authenticated"},
        404: {"description": "Session not found"},
    },
)
async def process_frame(
    session_id: str,
    frame_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
):
    """
    Process a single frame of video for sign language recognition.

    - `session_id`: The ID of the active session
    - `frame_data`: Frame data including image and metadata

    Returns the detected signs and current transcription state.
    """
    # STUB: Implement real-time frame processing
    # This would integrate with computer vision pipeline
    return {
        "session_id": session_id,
        "confidence": 0.85,
        "detected_signs": [
            {"sign": "hello", "confidence": 0.9},
            {"sign": "world", "confidence": 0.8},
        ],
        "transcribed_text": "Hello world",
        "timestamp": datetime.now(settings.TZ),
    }


@router.post(
    "/end-session",
    summary="End an active transcription session",
    responses={
        200: {"description": "Session ended successfully"},
        400: {"description": "Invalid session ID"},
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized to end this session"},
        404: {"description": "Session not found"},
    },
)
async def end_transcription_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Properly close a transcription session and clean up resources.

    - `session_id`: The ID of the session to end

    Returns a confirmation of session termination.
    """
    # STUB: Implement session cleanup and final processing
    return {"message": "Session ended", "session_id": session_id}
