# Widle Insure Platform (Alpha)

AI-Automated Auto Insurance Claims Platform.

## Architecture

*   **Backend**: FastAPI, PostgreSQL, Redis, Celery (Todo), LangChain (Todo)
*   **Frontend**: Next.js 14, Shadcn UI, Tailwind CSS
*   **AI**: Claude 4.5 Sonnet (Planned), Computer Vision (Planned)

## Prerequisites

*   Docker & Docker Compose
*   Python 3.11+
*   Node.js 20+

## Quick Start

1.  **Start Infrastructure**:
    ```bash
    docker compose up -d
    ```

2.  **Backend Setup**:
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cp ../.env.example ../.env
    alembic -c backend/alembic.ini upgrade head
    python backend/seed_data.py
    uvicorn app.main:app --reload
    ```
    Health Check: [http://localhost:8000/health](http://localhost:8000/health)

3.  **Frontend Setup**:
    ```bash
    cd frontend
    cp .env.example .env.local
    npm install
    npm run dev
    ```
    App: [http://localhost:3000](http://localhost:3000)

## Week 1 Deliverables (Completed)
*   [x] FastAPI Project Scaffolding
*   [x] PostgreSQL Schema & Migrations
*   [x] Next.js 14 + Shadcn UI Setup
*   [x] Backend <-> Frontend Connection
