from pydantic import BaseModel

class ExerciseOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    instructions: str | None = None
    target_muscles: str | None = None
    equipment: str | None = None
    difficulty: str | None = None

    class Config:
        from_attributes = True