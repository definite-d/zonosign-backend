# routers/curriculum.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Module, Lesson, User
from schemas import ModuleResponse, LessonResponse
from routers.users import get_current_user

router = APIRouter()

@router.get(
    "/modules",
    response_model=List[ModuleResponse],
    summary="Get all active modules",
    responses={
        200: {"description": "List of active modules retrieved successfully"},
        401: {"description": "Not authenticated"}
    }
)
async def get_modules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all active learning modules in the curriculum.
    
    Modules are returned in the order specified by their `order_index`.
    Only active modules (where `is_active` is True) are included.
    """
    modules = db.query(Module).filter(Module.is_active == True).order_by(Module.order_index).all()
    return modules

@router.get(
    "/modules/{module_id}",
    response_model=ModuleResponse,
    summary="Get a specific module by ID",
    responses={
        200: {"description": "Module retrieved successfully"},
        401: {"description": "Not authenticated"},
        404: {"description": "Module not found or inactive"}
    }
)
async def get_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve details of a specific learning module.
    
    Args:
        module_id: The ID of the module to retrieve
        
    Returns the module details if found and active, otherwise returns 404.
    """
    module = db.query(Module).filter(Module.id == module_id, Module.is_active == True).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

@router.get(
    "/modules/{module_id}/lessons",
    response_model=List[LessonResponse],
    summary="Get all lessons in a module",
    responses={
        200: {"description": "List of lessons retrieved successfully"},
        401: {"description": "Not authenticated"},
        404: {"description": "Module not found or inactive"}
    }
)
async def get_module_lessons(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all active lessons within a specific module.
    
    Args:
        module_id: The ID of the parent module
        
    Returns a list of active lessons in the module, ordered by their `order_index`.
    """
    # Verify module exists and is active
    module = db.query(Module).filter(Module.id == module_id, Module.is_active == True).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
        
    lessons = db.query(Lesson).filter(
        Lesson.module_id == module_id,
        Lesson.is_active == True
    ).order_by(Lesson.order_index).all()
    return lessons

@router.get(
    "/modules/{module_id}/lessons/{lesson_id}",
    response_model=LessonResponse,
    summary="Get a specific lesson",
    responses={
        200: {"description": "Lesson retrieved successfully"},
        401: {"description": "Not authenticated"},
        404: {"description": "Lesson or module not found or inactive"}
    }
)
async def get_lesson(
    module_id: int,
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve details of a specific lesson within a module.
    
    Args:
        module_id: The ID of the parent module
        lesson_id: The ID of the lesson to retrieve
        
    Returns the lesson details if found, active, and belonging to the specified module.
    Otherwise, returns 404.
    """
    # Verify module exists and is active
    module = db.query(Module).filter(Module.id == module_id, Module.is_active == True).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
        
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.module_id == module_id,
        Lesson.is_active == True
    ).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

