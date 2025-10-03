from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.workout_plan import WorkoutPlan
from app.models.plan_item import PlanItem
from app.models.exercise import Exercise
from app.schemas.workout_plan import (
    WorkoutPlanCreate,
    WorkoutPlanUpdate,
    WorkoutPlanOut,
    PlanItemCreate,
    PlanItemUpdate,
    PlanItemOut,
)
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/plans",
    tags=["Workout Plans"]
)

# Workout Plan Endpoints

@router.post("/", response_model=WorkoutPlanOut, summary="Create a new workout plan")
def create_plan(
    plan_in: WorkoutPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = WorkoutPlan(
        user_id=current_user.id,
        title=plan_in.title,
        goal_text=plan_in.goal_text,
        frequency_per_week=plan_in.frequency_per_week,
        session_duration_minutes=plan_in.session_duration_minutes,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.get("/", response_model=List[WorkoutPlanOut], summary="List my workout plans")
def list_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(WorkoutPlan).filter(WorkoutPlan.user_id == current_user.id).all()


@router.get("/{plan_id}", response_model=WorkoutPlanOut, summary="Get a workout plan by ID")
def get_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.id == plan_id, WorkoutPlan.user_id == current_user.id)
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.patch("/{plan_id}", response_model=WorkoutPlanOut, summary="Update a workout plan")
def update_plan(
    plan_id: int,
    plan_in: WorkoutPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.id == plan_id, WorkoutPlan.user_id == current_user.id)
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    plan.title = plan_in.title
    plan.goal_text = plan_in.goal_text
    plan.frequency_per_week = plan_in.frequency_per_week
    plan.session_duration_minutes = plan_in.session_duration_minutes

    db.commit()
    db.refresh(plan)
    return plan


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a workout plan")
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.id == plan_id, WorkoutPlan.user_id == current_user.id)
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    db.delete(plan)
    db.commit()
    return None


# Plan Item Endpoints

@router.post("/{plan_id}/items", response_model=PlanItemOut, summary="Add exercise to a plan")
def add_item(
    plan_id: int,
    item_in: PlanItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.id == plan_id, WorkoutPlan.user_id == current_user.id)
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    exercise = db.query(Exercise).filter(Exercise.id == item_in.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # Determine order_index
    if item_in.order_index is None:
        max_order = db.query(PlanItem).filter(PlanItem.plan_id == plan.id).count()
        order_index = max_order + 1
    else:
        order_index = item_in.order_index
        # Shift later items down
        db.query(PlanItem).filter(
            PlanItem.plan_id == plan.id,
            PlanItem.order_index >= order_index
        ).update({PlanItem.order_index: PlanItem.order_index + 1})
        db.commit()

    item = PlanItem(
        plan_id=plan.id,
        exercise_id=item_in.exercise_id,
        sets=item_in.sets,
        reps=item_in.reps,
        duration_seconds=item_in.duration_seconds,
        distance_meters=item_in.distance_meters,
        order_index=order_index,
        notes=item_in.notes,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{plan_id}/items/{item_id}", response_model=PlanItemOut, summary="Update an exercise in a plan")
def update_item(
    plan_id: int,
    item_id: int,
    item_in: PlanItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.id == plan_id, WorkoutPlan.user_id == current_user.id)
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    item = db.query(PlanItem).filter(PlanItem.id == item_id, PlanItem.plan_id == plan.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Handle reordering
    if item_in.order_index is not None and item_in.order_index != item.order_index:
        new_index = item_in.order_index
        old_index = item.order_index

        if new_index < old_index:
            db.query(PlanItem).filter(
                PlanItem.plan_id == plan.id,
                PlanItem.order_index >= new_index,
                PlanItem.order_index < old_index,
                PlanItem.id != item.id
            ).update({PlanItem.order_index: PlanItem.order_index + 1})
        elif new_index > old_index:
            db.query(PlanItem).filter(
                PlanItem.plan_id == plan.id,
                PlanItem.order_index <= new_index,
                PlanItem.order_index > old_index,
                PlanItem.id != item.id
            ).update({PlanItem.order_index: PlanItem.order_index - 1})

        item.order_index = new_index

    # Update other fields
    item.sets = item_in.sets
    item.reps = item_in.reps
    item.duration_seconds = item_in.duration_seconds
    item.distance_meters = item_in.distance_meters
    item.notes = item_in.notes

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{plan_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove an exercise from a plan")
def delete_item(
    plan_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.id == plan_id, WorkoutPlan.user_id == current_user.id)
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    item = db.query(PlanItem).filter(PlanItem.id == item_id, PlanItem.plan_id == plan.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    deleted_order = item.order_index
    db.delete(item)
    db.commit()

    db.query(PlanItem).filter(
        PlanItem.plan_id == plan.id,
        PlanItem.order_index > deleted_order
    ).update({PlanItem.order_index: PlanItem.order_index - 1})
    db.commit()

    return None
