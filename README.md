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

## Local Setup Guide

## Requirements
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- PostgreSQL Client (e.g., TablePlus)

## Part 1: Backend Setup (FastAPI)

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. **Start Infrastructure (PostgreSQL, Redis):**
   ```bash
   docker compose up -d
   ```

3. **Python Environment:**
   Navigate to the backend directory, create a virtual environment, and install dependencies.
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Copy the example environment file and customize it.
   ```bash
   cp ../.env.example ../.env
   ```
   Ensure `DATABASE_URL` is set correctly to your local PostgreSQL instance provided by Docker (e.g., `postgresql+asyncpg://postgres:postgres@localhost:5432/insurance`).

5. **Database Migrations:**
   Run Alembic to apply the latest database schema migrations.
   ```bash
   alembic -c backend/alembic.ini upgrade head
   ```

6. **Seed Test Data (Optional but Recommended):**
   Populate the database with sample claims to test the application.
   ```bash
   python backend/seed_data.py
   ```

7. **Start the Development Server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   The backend should now be running at `http://localhost:8000`. You can test this by visiting the health check endpoint: `http://localhost:8000/health`.

## Part 2: Frontend Setup (Next.js)

1. **Node.js Environment:**
   Open a new terminal window and navigate to the frontend directory.
   ```bash
   cd frontend
   ```

2. **Install Dependencies:**
   ```bash
   npm install
   ```

3. **Environment Variables:**
   Copy the example environment file.
   ```bash
   cp .env.example .env.local
   ```
   Ensure `NEXT_PUBLIC_API_URL` is pointing to your local backend server (e.g., `http://localhost:8000/api/v1`).

4. **Start the Development Server:**
   ```bash
   npm run dev
   ```
   The frontend application should now be accessible at `http://localhost:3000`.

## Part 3: Linting and Testing

Before submitting any code, please ensure you run the project's formatters and linters.

**Backend:**
```bash
cd backend
ruff check .
pylint $(git ls-files '*.py')
pytest tests/
```

**Frontend:**
```bash
cd frontend
npm run lint
npm test
```

## Troubleshooting
- **"Port already in use":** Ensure no other instances of the backend/frontend are running using `lsof -i :8000` or `lsof -i :3000`. Kill existing processes if necessary.
- **"Connection Refused" (Database):** Check if Docker containers are running (`docker ps`). Verify `DATABASE_URL` in your `.env`.

## Week 1 Deliverables (Completed)
*   [x] FastAPI Project Scaffolding
*   [x] PostgreSQL Schema & Migrations
*   [x] Next.js 14 + Shadcn UI Setup
*   [x] Backend <-> Frontend Connection
