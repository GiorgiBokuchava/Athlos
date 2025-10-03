from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db import Base

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    title = Column(String(100), nullable=False)
    goal_text = Column(Text, nullable=True)
    frequency_per_week = Column(Integer, nullable=False)
    session_duration_minutes = Column(Integer, nullable=False)

    user = relationship("User", back_populates="plans")
    items = relationship("PlanItem", back_populates="plan", cascade="all, delete-orphan")