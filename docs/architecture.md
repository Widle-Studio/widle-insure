# Architecture Overview

The AI-Automated Auto Insurance Claims Platform is designed for rapid development, ease of deployment, and high reliability for its core functionality: First Notice of Loss (FNOL) processing, automated damage assessment, fraud detection, and fast payouts.

## High-Level Architecture Diagram

```mermaid
graph TD;
    User[Claimant (Web UI)] --> Frontend[Frontend (Next.js)]
    Admin[Admin (Web Dashboard)] --> Frontend
    Frontend --> API[Backend API (FastAPI)]

    API --> DB[(PostgreSQL)]
    API --> Storage[(S3 / R2 Photo Storage)]

    API --> AI[Claude Vision API]
    API --> RulesEngine[Adjudication Engine]
    API --> FraudDetection[Fraud Detection Engine]

    RulesEngine --> PaymentGateway[Stripe Payouts]
    FraudDetection --> Admin
```

## Core Components

### 1. Frontend (Next.js 14+)
The frontend is built using Next.js 14, providing a fast, server-rendered React application.
- **UI Framework:** Shadcn UI + Tailwind CSS for a clean, accessible, and highly customizable insurance-friendly interface.
- **Key Modules:**
  - **FNOL Intake Form:** Multi-step wizard for claimants to submit accident details and photos.
  - **Admin Dashboard:** Claims management interface with analytics, AI review, and manual override capabilities.
  - **Claimant Portal:** Simple status lookup for claimants to track progress and payout details.

### 2. Backend (FastAPI)
The backend is powered by FastAPI, offering high performance, automatic OpenAPI documentation, and asynchronous processing.
- **Language:** Python 3.11+
- **Database ORM:** SQLAlchemy with Alembic for migrations.
- **Authentication:** JWT-based authentication for the admin dashboard (Clerk for MVP).
- **Core Responsibilities:** Data validation, business logic, interacting with external APIs, and managing the core workflow states.

### 3. AI & Analysis Engine
The platform integrates advanced AI capabilities to automate damage assessment and decision-making.
- **Model:** Claude 4.5 Sonnet (Primary) or GPT-4o.
- **Functionality:** Analyzes uploaded incident photos to determine damage severity, identify affected parts, calculate estimated repair costs, and flag potential fraud indicators.
- **Adjudication Engine:** deterministic rule-based engine that auto-approves simple claims (<$2000, high AI confidence, no red flags) and routes complex cases to the human review queue.

### 4. Data Layer
- **Relational Database:** PostgreSQL (Supabase for MVP, AWS RDS for Production).
- **Blob Storage:** S3/R2 for securely storing claimant photos and generating signed URLs for secure access.

### 5. Payments & Notifications
- **Payment Gateway:** Stripe Connect for initiating payouts to claimants upon claim approval.
- **Notifications:** Email infrastructure (SendGrid/Resend) for keeping claimants updated at key stages (intake, approval, payout, rejection).