"""
Authentication endpoints for the Athlos API.

- **Register** a new user
- **Login** with email + password to get a JWT
- **Get current user** details with a valid JWT

Use the `Authorization: Bearer <token>` header for protected endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import jwt

from app.db import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.config import settings

# Router setup
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={401: {"description": "Not authorized"}},
)

# Extract JWT from the Authorization header
oauth2_scheme = APIKeyHeader(name="Authorization")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_minutes: int = 60):
    """
    Create a signed JWT token with an expiry time (default 60 minutes).
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")


@router.post(
    "/register",
    response_model=UserOut,
    summary="Register a new user",
    description="Create a new user account with email and password. Passwords are hashed using bcrypt."
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Example request:
    ```
    {
      "email": "newuser@example.com",
      "password": "mypassword123"
    }
    ```

    Example response:
    ```
    {
      "id": 1,
      "email": "newuser@example.com"
    }
    ```
    """
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Enforce bcrypt 72-byte limit
    if len(user.password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="Password too long (max 72 bytes for bcrypt)")

    new_user = User(
        email=user.email,
        password_hash=User.hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    summary="Authenticate user and get a JWT",
    description="Authenticate using email and password. Returns a JWT token."
)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Example request:
    ```
    {
      "email": "newuser@example.com",
      "password": "mypassword123"
    }
    ```

    Example response:
    ```
    {
      "access_token": "jwt_string_here",
      "token_type": "bearer"
    }
    ```

    Use the JWT in subsequent requests:

    ```
    Authorization: Bearer <your_token>
    ```
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependency to extract and validate the current user from a JWT token.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get current user info",
    description="Return details of the currently authenticated user."
)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Example response:
    ```
    {
      "id": 1,
      "email": "newuser@example.com"
    }
    ```

    Requires a valid JWT in the `Authorization` header:

    ```
    Authorization: Bearer <your_token>
    ```
    """
    return current_user
