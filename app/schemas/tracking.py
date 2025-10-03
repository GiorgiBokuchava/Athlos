from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


# Workout Log Schemas

class WorkoutLogBase(BaseModel):
    log_date: date = Field(..., example="2025-10-03")
    notes: Optional[str] = Field(None, example="Felt strong today, pushed extra reps")


class WorkoutLogCreate(WorkoutLogBase):
    plan_id: Optional[int] = Field(None, example=1, description="WorkoutPlan ID (optional)")


class WorkoutLogOut(WorkoutLogBase):
    id: int
    user_id: int
    plan_id: Optional[int] = None

    class Config:
        from_attributes = True


# Weight Log Schemas

class WeightLogBase(BaseModel):
    log_date: date = Field(..., example="2025-10-03")
    weight: float = Field(..., example=72.5, description="Weight in kilograms")


class WeightLogCreate(WeightLogBase):
    pass


class WeightLogOut(WeightLogBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# Goal Schemas

class GoalBase(BaseModel):
    type: str = Field(..., example="weight", description="Either 'weight' or 'exercise'")
    target_value: float = Field(..., example=70.0, description="Target weight (kg) or reps/distance")
    deadline: Optional[date] = Field(None, example="2025-12-31")


class GoalCreate(GoalBase):
    exercise_id: Optional[int] = Field(None, example=2, description="Exercise ID (only for type=exercise)")


class GoalUpdate(GoalBase):
    exercise_id: Optional[int] = None


class GoalOut(GoalBase):
    id: int
    user_id: int
    exercise_id: Optional[int] = None

    class Config:
        from_attributes = True