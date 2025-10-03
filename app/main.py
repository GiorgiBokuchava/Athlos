from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db import get_db
from app.routers import auth, exercises, plans, tracking, workout_mode

app = FastAPI(title="Athlos API")

app.include_router(auth.router)
app.include_router(exercises.router)
app.include_router(plans.router)
app.include_router(tracking.router)
app.include_router(workout_mode.router)

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

@app.get("/")
def root():
    return {"message": "Athlos API is running 🚀"}