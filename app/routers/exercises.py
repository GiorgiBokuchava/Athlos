from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseOut
from typing import List

router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"]
)

@router.get(
    "/",
    response_model=List[ExerciseOut],
    summary="List all exercises",
    description="Retrieve a list of all predefined exercises available in the system.",
    responses={
        200: {
            "description": "A list of exercises",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Push-Up",
                            "description": "A bodyweight exercise that strengthens the chest, shoulders, and triceps.",
                            "instructions": "Keep body straight, lower chest to floor, push back up.",
                            "target_muscles": "Chest, Shoulders, Triceps",
                            "equipment": "None",
                            "difficulty": "Beginner"
                        },
                        {
                            "id": 2,
                            "name": "Squat",
                            "description": "A lower body exercise targeting quadriceps and glutes.",
                            "instructions": "Stand with feet shoulder-width apart, bend knees and hips, return to standing.",
                            "target_muscles": "Quadriceps, Glutes, Hamstrings",
                            "equipment": "None",
                            "difficulty": "Beginner"
                        }
                    ]
                }
            }
        }
    }
)
def list_exercises(db: Session = Depends(get_db)):
    return db.query(Exercise).all()

@router.get(
    "/{exercise_id}",
    response_model=ExerciseOut,
    summary="Get exercise by ID",
    description="Retrieve detailed information about a specific exercise using its ID.",
    responses={
        200: {
            "description": "Exercise found",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Push-Up",
                        "description": "A bodyweight exercise that strengthens the chest, shoulders, and triceps.",
                        "instructions": "Keep body straight, lower chest to floor, push back up.",
                        "target_muscles": "Chest, Shoulders, Triceps",
                        "equipment": "None",
                        "difficulty": "Beginner"
                    }
                }
            }
        },
        404: {"description": "Exercise not found"}
    }
)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise
