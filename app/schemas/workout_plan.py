from pydantic import BaseModel, Field
from typing import List, Optional


# Plan Item Schemas

class PlanItemBase(BaseModel):
    sets: Optional[int] = Field(None, example=3)
    reps: Optional[int] = Field(None, example=12)
    duration_seconds: Optional[int] = Field(None, example=300, description="Duration in seconds")
    distance_meters: Optional[int] = Field(None, example=1000, description="Distance in meters")
    order_index: Optional[int] = Field(None, example=1, description="Order of the exercise in the plan")
    notes: Optional[str] = Field(None, example="Keep core tight during the movement")


class PlanItemCreate(PlanItemBase):
    exercise_id: int = Field(..., example=1, description="ID of the exercise to add")


class PlanItemUpdate(PlanItemBase):
    pass


class PlanItemOut(PlanItemBase):
    id: int
    exercise_id: int

    class Config:
        from_attributes = True


# Workout Plan Schemas

class WorkoutPlanBase(BaseModel):
    title: str = Field(..., example="Strength Training Plan")
    goal_text: Optional[str] = Field(None, example="Increase muscle strength")
    frequency_per_week: int = Field(..., example=3)
    session_duration_minutes: int = Field(..., example=60)


class WorkoutPlanCreate(WorkoutPlanBase):
    pass


class WorkoutPlanUpdate(WorkoutPlanBase):
    pass


class WorkoutPlanOut(WorkoutPlanBase):
    id: int
    user_id: int
    items: List[PlanItemOut] = []

    class Config:
        from_attributes = True
