from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.routers import auth

app = FastAPI(title="Athlos API")

app.include_router(auth.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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