# Deployment Guide

The AI-Automated Auto Insurance Claims Platform is designed for rapid deployment using modern cloud infrastructure.

## Infrastructure Architecture

The platform consists of three main components:
1. **Frontend (Next.js):** Hosted on Vercel
2. **Backend (FastAPI):** Hosted on Railway/Render (or AWS/Vercel for Production)
3. **Database (PostgreSQL):** Hosted on Supabase (MVP) or AWS RDS (Production)

## Prerequisites

Before deploying the platform, you will need accounts with:
- GitHub (to host the repository)
- Vercel (Frontend Hosting)
- Railway / Render (Backend Hosting)
- Supabase (PostgreSQL Database)
- Stripe (Payments)

## Step-by-Step Deployment Guide

### 1. Database (Supabase)

1. Create a new project in Supabase.
2. In your Supabase dashboard, copy the PostgreSQL connection string.
3. This connection URL will be used in your Backend environment variables (`DATABASE_URL`).

### 2. Backend (Railway/Render)

1. Connect your GitHub repository to Railway or Render.
2. Create a new web service and select the `backend` folder as the root directory.
3. Add the following environment variables:
   - `DATABASE_URL`: The PostgreSQL connection string from Supabase.
   - `SECRET_KEY`: A secure random string for JWT encoding.
   - `STRIPE_SECRET_KEY`: Your Stripe test/live API key.
   - `ANTHROPIC_API_KEY`: Your Claude API key.
4. Deploy the service.
5. Once deployed, note the Public URL (e.g., `https://backend-your-app.railway.app`).

### 3. Frontend (Vercel)

1. Connect your GitHub repository to Vercel.
2. Select the `frontend` directory as the project root.
3. Vercel will automatically detect the Next.js framework.
4. Add the following environment variables:
   - `NEXT_PUBLIC_API_URL`: The Public URL of your deployed Backend service.
5. Deploy the application.
6. Note the final frontend domain (e.g., `https://your-app.vercel.app`).

## Verifying Deployment

1. Visit the final Vercel frontend domain in your browser.
2. Try submitting a test claim through the FNOL form.
3. Verify that the backend successfully created the claim in the Supabase database.
4. Confirm that the AI analysis ran successfully and the result is available in the admin dashboard.