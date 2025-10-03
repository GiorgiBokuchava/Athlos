from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.workout_log import WorkoutLog
from app.models.weight_log import WeightLog
from app.models.goal import Goal
from app.schemas.tracking import (
    WorkoutLogCreate, WorkoutLogOut,
    WeightLogCreate, WeightLogOut,
    GoalCreate, GoalUpdate, GoalOut
)
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/tracking",
    tags=["Tracking & Goals"]
)

# Workout Logs

@router.post(
    "/workouts",
    response_model=WorkoutLogOut,
    summary="Log a completed workout",
    description="Create a new workout log entry for the current user.",
    responses={
        200: {
            "description": "Workout log created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "user_id": 1,
                        "plan_id": 2,
                        "log_date": "2025-10-03",
                        "notes": "Felt strong today, pushed extra reps"
                    }
                }
            }
        }
    }
)
def create_workout_log(
    log_in: WorkoutLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = WorkoutLog(
        user_id=current_user.id,
        plan_id=log_in.plan_id,
        log_date =log_in.log_date,
        notes=log_in.notes
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get(
    "/workouts",
    response_model=List[WorkoutLogOut],
    summary="List my workout logs",
    description="Retrieve all workout logs for the current user.",
    responses={
        200: {
            "description": "List of workout logs",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "user_id": 1,
                            "plan_id": 2,
                            "log_date": "2025-10-01",
                            "notes": "Leg day, tough but good."
                        },
                        {
                            "id": 2,
                            "user_id": 1,
                            "plan_id": 3,
                            "log_date": "2025-10-02",
                            "notes": "Upper body strength session."
                        }
                    ]
                }
            }
        }
    }
)
def list_workout_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(WorkoutLog).filter(WorkoutLog.user_id == current_user.id).all()


@router.get(
    "/workouts/{log_id}",
    response_model=WorkoutLogOut,
    summary="Get a workout log by ID",
    description="Retrieve details of a specific workout log belonging to the current user.",
    responses={
        200: {
            "description": "Workout log found",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "user_id": 1,
                        "plan_id": 2,
                        "log_date": "2025-10-03",
                        "notes": "PR on squats today."
                    }
                }
            }
        },
        404: {"description": "Workout log not found"}
    }
)
def get_workout_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = db.query(WorkoutLog).filter(
        WorkoutLog.id == log_id,
        WorkoutLog.user_id == current_user.id
    ).first()
    if not log:
        raise HTTPException(status_code=404, detail="Workout log not found")
    return log


@router.delete(
    "/workouts/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a workout log",
    description="Delete a specific workout log belonging to the current user.",
    responses={
        204: {"description": "Workout log deleted successfully"},
        404: {"description": "Workout log not found"}
    }
)
def delete_workout_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = db.query(WorkoutLog).filter(
        WorkoutLog.id == log_id,
        WorkoutLog.user_id == current_user.id
    ).first()
    if not log:
        raise HTTPException(status_code=404, detail="Workout log not found")

    db.delete(log)
    db.commit()
    return None


# Weight Logs

@router.post(
    "/weights",
    response_model=WeightLogOut,
    summary="Add a weight entry",
    description="Record a new weight log for the current user.",
    responses={
        200: {
            "description": "Weight log created",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "user_id": 1,
                        "log_date": "2025-10-03",
                        "weight": 72.5
                    }
                }
            }
        }
    }
)
def create_weight_log(
    log_in: WeightLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = WeightLog(
        user_id=current_user.id,
        log_date=log_in.log_date,
        weight=log_in.weight
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get(
    "/weights",
    response_model=List[WeightLogOut],
    summary="List my weight history",
    description="Retrieve all weight log entries for the current user.",
    responses={
        200: {
            "description": "List of weight logs",
            "content": {
                "application/json": {
                    "example": [
                        {"id": 1, "user_id": 1, "log_date": "2025-09-30", "weight": 74.0},
                        {"id": 2, "user_id": 1, "log_date": "2025-10-01", "weight": 73.0},
                        {"id": 3, "user_id": 1, "log_date": "2025-10-02", "weight": 72.5}
                    ]
                }
            }
        }
    }
)
def list_weight_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(WeightLog).filter(WeightLog.user_id == current_user.id).all()


@router.delete(
    "/weights/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a weight entry",
    description="Delete a weight log entry belonging to the current user.",
    responses={
        204: {"description": "Weight log deleted successfully"},
        404: {"description": "Weight log not found"}
    }
)
def delete_weight_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = db.query(WeightLog).filter(
        WeightLog.id == log_id,
        WeightLog.user_id == current_user.id
    ).first()
    if not log:
        raise HTTPException(status_code=404, detail="Weight log not found")

    db.delete(log)
    db.commit()
    return None


# Goals

@router.post(
    "/goals",
    response_model=GoalOut,
    summary="Set a new goal",
    description="Create a new goal (weight or exercise achievement).",
    responses={
        200: {
            "description": "Goal created",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "user_id": 1,
                        "type": "weight",
                        "target_value": 70.0,
                        "deadline": "2025-12-31",
                        "exercise_id": None
                    }
                }
            }
        }
    }
)
def create_goal(
    goal_in: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = Goal(
        user_id=current_user.id,
        type=goal_in.type,
        target_value=goal_in.target_value,
        deadline=goal_in.deadline,
        exercise_id=goal_in.exercise_id
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


@router.get(
    "/goals",
    response_model=List[GoalOut],
    summary="List my goals",
    description="Retrieve all fitness goals for the current user.",
    responses={
        200: {
            "description": "List of goals",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "user_id": 1,
                            "type": "weight",
                            "target_value": 70.0,
                            "deadline": "2025-12-31",
                            "exercise_id": None
                        },
                        {
                            "id": 2,
                            "user_id": 1,
                            "type": "exercise",
                            "target_value": 100.0,
                            "deadline": None,
                            "exercise_id": 5
                        }
                    ]
                }
            }
        }
    }
)
def list_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Goal).filter(Goal.user_id == current_user.id).all()


@router.patch(
    "/goals/{goal_id}",
    response_model=GoalOut,
    summary="Update a goal",
    description="Update an existing goal belonging to the current user.",
    responses={
        200: {
            "description": "Goal updated",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "user_id": 1,
                        "type": "exercise",
                        "target_value": 120.0,
                        "deadline": "2026-01-01",
                        "exercise_id": 3
                    }
                }
            }
        },
        404: {"description": "Goal not found"}
    }
)
def update_goal(
    goal_id: int,
    goal_in: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    goal.type = goal_in.type
    goal.target_value = goal_in.target_value
    goal.deadline = goal_in.deadline
    goal.exercise_id = goal_in.exercise_id

    db.commit()
    db.refresh(goal)
    return goal


@router.delete(
    "/goals/{goal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a goal",
    description="Delete a goal belonging to the current user.",
    responses={
        204: {"description": "Goal deleted successfully"},
        404: {"description": "Goal not found"}
    }
)
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    db.delete(goal)
    db.commit()
    return None
