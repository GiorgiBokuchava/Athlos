from sqlalchemy import Column, Integer, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from app.db import Base

class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(Integer, ForeignKey("workout_plans.id", ondelete="SET NULL"), nullable=True)

    log_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="workout_logs")
    plan = relationship("WorkoutPlan")