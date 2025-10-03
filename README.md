# Athlos 🏋️

A RESTful API built with FastAPI for managing workout plans, tracking fitness goals, and guiding workout sessions. Implements authentication, predefined exercises, personalized plans, tracking, workout mode, and comes with Docker support for easy deployment.

## ✨ Features

- **User Authentication** – Register, login, and secure endpoints with JWT.
- **Predefined Exercises** – Database seeded with 20+ exercises.
- **Personalized Workout Plans** – Create plans, add/remove exercises, customize reps/sets/duration.
- **Tracking & Goals** – Log workouts, track weight, set fitness goals.
- **Workout Mode** – Guided session with step-by-step exercise progression.
- **Swagger Docs** – Interactive API documentation at `/docs`.
- **Dockerized** – One command to spin up backend + PostgreSQL.

## 📂 Project Structure

```
Athlos/
├── alembic/              # Database migrations
├── app/
│   ├── models/           # SQLAlchemy models
│   ├── routers/          # API routes
│   ├── schemas/          # Pydantic schemas
│   ├── seed_exercises.py # Script to seed database with exercises
│   ├── db.py             # Database connection
│   ├── config.py         # Settings loader
│   └── main.py           # FastAPI entrypoint
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## ⚙️ Local Setup (without Docker)

1. **Clone and enter project**
   ```
   git clone https://github.com/GiorgiBokuchava/Athlos.git
   cd Athlos
   ```

2. **Create and activate virtual environment**
   ```
   python -m venv env
   source env/bin/activate   # Linux/Mac
   env\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Configure `.env`**

   Copy the example file:
   ```
   cp .env.example .env
   ```

   Set the following:
   - `DATABASE_URL` → PostgreSQL connection string.  
     Example:  
     `postgresql+psycopg2://postgres:postgres@localhost:5432/athlos`
   - `JWT_SECRET` → any random string for signing JWT tokens.  
     Example:  
     `JWT_SECRET=supersecret`

5. **Run migrations**
   ```
   alembic upgrade head
   ```

6. **Seed exercises**
   ```
   python -m app.seed_exercises
   ```

7. **Start app**
   ```
   uvicorn app.main:app --reload
   ```

   Docs → http://127.0.0.1:8000/docs

## 🐳 Running with Docker

1. **Clone repo**
   ```
   git clone https://github.com/GiorgiBokuchava/Athlos.git
   cd Athlos
   ```

2. **Copy `.env.example` to `.env`**
   ```
   cp .env.example .env
   ```

   Default values:  
   - `DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/athlos`  
   - `JWT_SECRET=your_jwt_secret_key`

   Works with the bundled Postgres container (`db`).  
   Or point `DATABASE_URL` to your own PostgreSQL server.

3. **Build and run**
   ```
   docker compose up --build
   ```

   Runs:  
   - `backend` → FastAPI at http://localhost:8000  
   - `db` → PostgreSQL at localhost:5432

4. **Seed exercises**
   ```
   docker compose exec backend python -m app.seed_exercises
   ```

5. **Access Swagger**  
   👉 http://localhost:8000/docs

## 📖 API Overview

### 🔑 Authentication

- `POST /auth/register` – Register new user
- `POST /auth/login` – Get JWT token
- `GET /auth/me` – Current user info

### 🏋️ Exercises

- `GET /exercises/` – List all exercises
- `GET /exercises/{id}` – Get exercise by ID

### 📋 Workout Plans

- `POST /plans/` – Create new plan
- `GET /plans/` – List my plans
- `GET /plans/{id}` – Get plan with exercises
- `PATCH /plans/{id}` – Update plan
- `DELETE /plans/{id}` – Delete plan
- `POST /plans/{id}/items` – Add exercise to plan
- `PATCH /plans/{id}/items/{item_id}` – Update plan item
- `DELETE /plans/{id}/items/{item_id}` – Remove exercise

### 📈 Tracking & Goals

- `POST /tracking/workouts` – Log workout
- `GET /tracking/workouts` – List workout logs
- `POST /tracking/weights` – Add weight log
- `GET /tracking/weights` – List weight logs
- `POST /tracking/goals` – Set a goal
- `GET /tracking/goals` – List goals

### ▶️ Workout Mode

- `POST /workout-mode/start/{plan_id}` – Start session, get first exercise
- `PATCH /workout-mode/{session_id}/complete` – Mark current exercise complete, return next
- `POST /workout-mode/{session_id}/finish` – Finish session

## 🧪 Testing in Swagger

Go to `/docs`.  

Register → Login → Authorize with JWT.  

Try endpoints in order:  
- Create plan, add exercises.  
- Log workouts, add weight, set goals.  
- Start workout mode and step through exercises.

## 📝 Seeding

The seeding script inserts 20+ predefined exercises (push-ups, squats, pull-ups, etc.).  


Run locally:  
```
python -m app.seed_exercises
```

Run inside Docker:  
```
docker compose exec backend python -m app.seed_exercises
```

## 🔒 Security

- JWT-based authentication.
- Passwords hashed with bcrypt (never stored in plain text).

- Protected endpoints require `Authorization: Bearer <token>`.

