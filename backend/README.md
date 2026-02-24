# Widle Insure Backend

FastAPI backend for the AI-Automated Auto Insurance Claims Platform.

## Setup

1.  **Dependencies**:
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Copy `.env.example` to `.env` in the root directory:
    ```bash
    cp ../.env.example ../.env
    ```
    Update `DATABASE_URL` if needed.

3.  **Database**:
    Ensure you have a PostgreSQL database running. For local development with Docker:
    ```bash
    docker compose up -d
    ```
    
    Run migrations:
    ```bash
    alembic -c backend/alembic.ini upgrade head
    ```

4.  **Seed Data**:
    ```bash
    python backend/seed_data.py
    ```

5.  **Run Server**:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.
    API Documentation: `http://localhost:8000/docs`

## Structure

*   `app/main.py`: Entry point
*   `app/models/`: SQLAlchemy models
*   `app/core/`: Configuration
*   `alembic/`: Database migrations

## Week 1 Tasks Completed
- [x] Project structure
- [x] Dependencies installed
- [x] Database schema defined
- [x] Alembic migrations configured
- [x] Health check endpoint
