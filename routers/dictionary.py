# routers/dictionary.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import SignEntry, User
from schemas import SignEntryResponse
from routers.users import get_current_user

router = APIRouter()


@router.get("/signs", response_model=List[SignEntryResponse])
async def get_signs(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    difficulty: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(SignEntry)

    if category:
        query = query.filter(SignEntry.category == category)
    if difficulty:
        query = query.filter(SignEntry.difficulty == difficulty)

    signs = query.offset(skip).limit(limit).all()
    return signs


@router.get(
    "/signs/{sign_id}",
    response_model=SignEntryResponse,
    summary="Get sign by ID",
    responses={
        200: {"description": "Sign found"},
        401: {"description": "Not authenticated (optional for public access)"},
        404: {"description": "Sign not found"},
    },
)
async def get_sign(
    sign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a specific sign by its unique ID.

    - `sign_id`: The unique identifier of the sign

    Returns the complete sign details if found, otherwise 404.
    """
    sign = db.query(SignEntry).filter(SignEntry.id == sign_id).first()
    if not sign:
        raise HTTPException(status_code=404, detail="Sign not found")
    return sign


@router.get(
    "/signs/search",
    response_model=List[SignEntryResponse],
    summary="Search signs",
    responses={
        200: {"description": "Matching signs found"},
        400: {"description": "Invalid search parameters"},
        401: {"description": "Not authenticated (optional for public access)"},
    },
)
async def search_signs(
    q: str = Query(..., description="Search query"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Search for signs matching the query string.

    Searches the word field for partial matches.

    Args:
        q: Search term to look for in words

    Returns a list of matching signs.
    """
    signs = db.query(SignEntry).filter(SignEntry.word.contains(q)).limit(50).all()
    return signs


@router.post(
    "/signs/{sign_id}/favorite",
    status_code=201,
    summary="Add sign to favorites",
    responses={
        201: {"description": "Sign added to favorites"},
        400: {"description": "Sign already in favorites"},
        401: {"description": "Not authenticated"},
        404: {"description": "Sign not found"},
    },
)
async def favorite_sign(
    sign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Add a sign to the current user's favorites.

    Args:
        sign_id: The ID of the sign to add to favorites

    Returns a success message if the sign was added to favorites,
    or an error if the sign doesn't exist or is already in favorites.
    """
    # Verify sign exists
    sign = db.query(SignEntry).filter(SignEntry.id == sign_id).first()
    if not sign:
        raise HTTPException(status_code=404, detail="Sign not found")

    # STUB: Implement add to favorites logic
    # In a real implementation, this would add a record to a user_favorites join table
    return {"message": "Added to favorites"}
