from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WorkoutSessionItem(BaseModel):
    id: int
    order_index: int
    exercise_name: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    duration_seconds: Optional[int] = None
    distance_meters: Optional[int] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class WorkoutSessionOut(BaseModel):
    id: int
    plan_id: int
    title: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    current_index: int
    current_exercise: Optional[WorkoutSessionItem] = None

    class Config:
        from_attributes = True


class CompleteItemRequest(BaseModel):
    notes: Optional[str] = Field(None, example="Reduced reps to 10, felt tough today")


class FinishSessionRequest(BaseModel):
    notes: Optional[str] = Field(None, example="Felt strong overall, PR on squats")
