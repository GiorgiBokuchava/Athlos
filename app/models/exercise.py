from sqlalchemy import Column, Integer, String, Text
from app.db import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    target_muscles = Column(String(200), nullable=True)
    equipment = Column(String(100), nullable=True)
    difficulty = Column(String(50), nullable=True)