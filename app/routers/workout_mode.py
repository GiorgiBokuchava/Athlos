from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app.models.workout_plan import WorkoutPlan
from app.models.plan_item import PlanItem
from app.models.workout_session import WorkoutSession
from app.models.workout_log import WorkoutLog
from app.schemas.workout_mode import WorkoutSessionOut, WorkoutSessionItem, CompleteItemRequest, FinishSessionRequest
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/workout-mode",
    tags=["Workout Mode"]
)

# Start a session
@router.post("/start/{plan_id}", response_model=WorkoutSessionOut)
def start_workout(plan_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.id == plan_id, WorkoutPlan.user_id == current_user.id
    ).first()
    if not plan:
        raise HTTPException(404, "Plan not found")

    # Prevent multiple active sessions
    existing = db.query(WorkoutSession).filter(
        WorkoutSession.user_id == current_user.id,
        WorkoutSession.plan_id == plan.id,
        WorkoutSession.ended_at.is_(None)
    ).first()
    if existing:
        raise HTTPException(400, "Session already active")

    session = WorkoutSession(user_id=current_user.id, plan_id=plan.id, current_index=1)
    db.add(session)
    db.commit()
    db.refresh(session)

    first_item = db.query(PlanItem).filter(PlanItem.plan_id == plan.id, PlanItem.order_index == 1).first()

    return WorkoutSessionOut(
        id=session.id,
        plan_id=plan.id,
        title=plan.title,
        started_at=session.started_at,
        ended_at=None,
        current_index=1,
        current_exercise=WorkoutSessionItem(
            id=first_item.id,
            order_index=first_item.order_index,
            exercise_name=first_item.exercise.name,
            sets=first_item.sets,
            reps=first_item.reps,
            duration_seconds=first_item.duration_seconds,
            distance_meters=first_item.distance_meters,
            notes=first_item.notes
        ) if first_item else None
    )

# Complete exercise
@router.patch("/{session_id}/complete", response_model=WorkoutSessionOut)
def complete_exercise(session_id: int, data: CompleteItemRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(WorkoutSession).filter(
        WorkoutSession.id == session_id, WorkoutSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(404, "Session not found")
    if session.ended_at:
        raise HTTPException(400, "Session already finished")

    item = db.query(PlanItem).filter(
        PlanItem.plan_id == session.plan_id,
        PlanItem.order_index == session.current_index
    ).first()
    if not item:
        raise HTTPException(404, "Exercise not found")

    log = WorkoutLog(
        user_id=current_user.id,
        plan_id=session.plan_id,
        log_date=func.current_date(),
        notes=f"Completed {item.exercise.name}: {data.notes or 'done'}"
    )
    db.add(log)

    session.current_index += 1
    db.commit()
    db.refresh(session)

    next_item = db.query(PlanItem).filter(
        PlanItem.plan_id == session.plan_id, PlanItem.order_index == session.current_index
    ).first()

    return WorkoutSessionOut(
        id=session.id,
        plan_id=session.plan_id,
        title=session.plan.title,
        started_at=session.started_at,
        ended_at=session.ended_at,
        current_index=session.current_index,
        current_exercise=WorkoutSessionItem(
            id=next_item.id,
            order_index=next_item.order_index,
            exercise_name=next_item.exercise.name,
            sets=next_item.sets,
            reps=next_item.reps,
            duration_seconds=next_item.duration_seconds,
            distance_meters=next_item.distance_meters,
            notes=next_item.notes
        ) if next_item else None
    )

# Finish session
@router.post("/{session_id}/finish")
def finish_session(session_id: int, data: FinishSessionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(WorkoutSession).filter(
        WorkoutSession.id == session_id, WorkoutSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(404, "Session not found")
    if session.ended_at:
        raise HTTPException(400, "Session already finished")

    session.ended_at = func.now()

    log = WorkoutLog(
        user_id=current_user.id,
        plan_id=session.plan_id,
        log_date=func.current_date(),
        notes=f"Session finished: {data.notes or 'No notes'}"
    )
    db.add(log)
    db.commit()
    db.refresh(session)

    return {"status": "finished", "session_id": session.id, "plan_id": session.plan_id, "notes": data.notes}
