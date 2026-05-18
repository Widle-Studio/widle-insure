# Widle Insure Platform (Alpha)

AI-Automated Auto Insurance Claims Platform.

---

## 1. High-Level Business Overview

**Platform Vision**
Widle Insure is an AI-native automobile insurance claim settlement platform. The goal is to automate the entire claims lifecycle—from First Notice of Loss (FNOL) intake, to damage assessment, fraud detection, and claim payout—with minimal human intervention.

**Key Objectives & Metrics**
- **Straight-Through Processing (STP):** Achieve a 70-80% STP rate within 6 months.
- **Accuracy:** Maintain 98%+ accuracy compared to human adjusters.
- **Speed:** Sub-24-hour claim settlement for simple cases.
- **Cost Efficiency:** Reduce processing cost to <$5 per claim (down from traditional $50-$150).

**Market Positioning**
The platform is positioned between traditional Business Process Outsourcing (BPOs) that are costly and slow, and enterprise platforms like Pace/Roots that are highly expensive. The initial target market is mid-size insurers and Managing General Agents (MGAs).

---

## 2. Technical Architecture Deep Dive

The platform utilizes a modern, cost-optimized, and AI-first tech stack.

### Frontend
- **Web Portal (Admin/Adjuster):** Built with **Next.js 14+** (React), using Shadcn UI and Tailwind CSS for styling. It handles the administrative dashboard, claims management, and human-in-the-loop review queues.
- **Mobile App (Claimant):** Built using **React Native (Expo)** to allow policyholders to easily submit claims and photos from iOS or Android devices.

### Backend Core
- **Framework:** **FastAPI (Python 3.11+)** chosen for its excellent async support, auto-documentation, and seamless integration with ML/AI libraries.
- **Database:** **PostgreSQL 15+** (via asyncpg and SQLAlchemy) for robust, ACID-compliant relational data storage.
- **Async Tasks & Caching:** **Redis** and **Celery** are utilized for background processing (like long-running AI inference) and caching.

### AI & Machine Learning Layer
- **Language Models (LLMs):** Primary integration with **Anthropic Claude 4.5 Sonnet** (via LangChain) for intent classification, FNOL intake summarization, and fraud analysis reasoning.
- **Computer Vision:** Custom fine-tuned **YOLOv8** models for local/cloud damage assessment (detecting severity and affected parts). Executed concurrently via `asyncio.to_thread` to prevent blocking the event loop.

### Infrastructure & Deployment
- **Hosting:** Multi-platform approach for cost-optimization. Next.js frontend deployed on **Vercel**; FastAPI backend deployed on **Vercel/Railway**.
- **Storage:** **AWS S3** (or compatible like Cloudflare R2) for storing claim photos and documents.
- **Integrations:** Stripe Connect for payouts, Resend/SendGrid for emails.

---

## 3. Features & Workflow

The Alpha platform covers the following end-to-end workflow:
1. **FNOL Intake:** User submits claim details and uploads damage photos via the Web/Mobile UI.
2. **Damage Assessment:** AI (Claude Vision / YOLOv8) analyzes photos, detects damaged parts, estimates severity, and calculates cost.
3. **Fraud Detection & Rules Engine:** ML-based and rule-based checks assess the claim for anomalies.
4. **Adjudication:** Simple claims under a certain threshold are auto-approved. Complex claims are routed to a human adjuster.
5. **Payout:** Automatic or manual trigger via Stripe Connect to pay out the approved claim amount.

---

## 4. Developer Onboarding Guide

Follow these steps to get your local development environment running.

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- PostgreSQL Client (e.g., TablePlus)

### Part 1: Backend Setup (FastAPI)

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
   Navigate to the backend directory, create a virtual environment, and install dependencies using `uv` (recommended) or `pip`.
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

### Part 2: Frontend Setup (Next.js)

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

### Part 3: Linting and Testing

Before submitting any code, please ensure you run the project's formatters, linters, and tests.

**Backend:**
```bash
cd backend
uv run ruff check .
uv run ruff format .
pytest tests/
```

**Frontend:**
```bash
cd frontend
npm run lint
npm run test
```

## Vercel Deployment

### Automatic Setup

1. **Connect to Vercel**: Push to GitHub, import in Vercel
2. **Add Vercel Postgres**: Dashboard → Storage → Create PostgreSQL
3. **Set Environment Variables**:
   ```
   FIRST_ADMIN_EMAIL=admin@widle.com
   FIRST_ADMIN_PASSWORD=your_secure_password
   ANTHROPIC_API_KEY=sk-ant-...
   SECRET_KEY=<generate with: openssl rand -hex 32>
   BACKEND_CORS_ORIGINS=https://your-app.vercel.app
   NEXT_PUBLIC_API_URL=https://your-app.vercel.app
   ```
4. **Deploy**: Migrations run automatically via postbuild script

### First Deployment

After first deployment:
- ✅ Database tables created automatically
- ✅ Admin user created with credentials from env vars
- ✅ Health check shows database status

### Manual Migration (if needed)

```bash
vercel env pull .env
cd backend
alembic upgrade head
python scripts/create_admin.py
```

## Troubleshooting
- **"Port already in use":** Ensure no other instances of the backend/frontend are running using `lsof -i :8000` or `lsof -i :3000`. Kill existing processes if necessary.
- **"Connection Refused" (Database):** Check if Docker containers are running (`docker ps`). Verify `DATABASE_URL` in your `.env`.
