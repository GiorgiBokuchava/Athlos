from sqlalchemy import Column, Integer, String
from app.db import Base
from passlib.context import CryptContext
from sqlalchemy.orm import relationship

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    plans = relationship("WorkoutPlan", back_populates="user", cascade="all, delete-orphan")

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        return  pwd_context.verify(password, self.password_hash)