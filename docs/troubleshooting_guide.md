# Troubleshooting Guide

Welcome to the AI-Automated Auto Insurance Claims Platform Troubleshooting Guide. This resource addresses common issues encountered during the alpha phase deployment and development.

## 1. Backend Service (FastAPI) Issues

### "Connection Refused" when accessing the API
*   **Symptom:** The frontend cannot reach the backend, or curl commands return `Connection refused`.
*   **Possible Causes:**
    *   The backend server (Uvicorn) is not running.
    *   The Docker containers (if using Docker Compose) are down.
    *   The `NEXT_PUBLIC_API_URL` environment variable in the frontend is incorrect.
*   **Solutions:**
    *   Verify the backend is running locally (`uvicorn app.main:app --reload` or `docker compose ps`).
    *   Check the backend logs for startup errors (e.g., missing environment variables or database connection failures).
    *   Ensure the frontend `.env.local` points to the correct backend URL (e.g., `http://localhost:8000/api/v1`).

### Database Migration Failures (Alembic)
*   **Symptom:** Running `alembic upgrade head` fails with an error about missing tables or syntax issues.
*   **Possible Causes:**
    *   The `DATABASE_URL` in your `.env` is incorrect or points to the wrong database.
    *   The PostgreSQL server is not running or accessible.
    *   A previous migration failed partially, leaving the database in an inconsistent state.
*   **Solutions:**
    *   Double-check the `DATABASE_URL` format: `postgresql+asyncpg://user:password@host:port/dbname`.
    *   Ensure the PostgreSQL service (Docker or Supabase) is active and accepting connections.
    *   If using local Docker, try tearing down and recreating the volume: `docker compose down -v` followed by `docker compose up -d`.

### AI Analysis (Claude API) Timeouts or Errors
*   **Symptom:** Claims are stuck in "Processing" state, or the AI analysis returns an error.
*   **Possible Causes:**
    *   The `ANTHROPIC_API_KEY` is missing or invalid.
    *   Rate limiting from the Anthropic API.
    *   The uploaded photos are too large or in an unsupported format.
*   **Solutions:**
    *   Verify the API key in the backend `.env` file.
    *   Check the backend logs for specific error messages from the Anthropic SDK.
    *   Implement retries or fallback logic (rule-based estimation) as outlined in the risk mitigation plan.

## 2. Frontend Application (Next.js) Issues

### "npm install" Failures or ETIMEDOUT
*   **Symptom:** Running `npm install` fails with network timeout errors or "Exit handler never called!".
*   **Possible Causes:**
    *   Network connectivity issues or a restricted development environment (e.g., behind a corporate proxy or offline sandbox).
*   **Solutions:**
    *   Ensure you have a stable internet connection.
    *   If in an offline environment (like the sandbox), rely on pre-installed dependencies. Do not attempt to run `npm install` if the environment lacks internet access; use mock scripts for verification instead.

### Changes Not Reflecting in Browser
*   **Symptom:** You've edited a React component, but the browser doesn't show the updates.
*   **Possible Causes:**
    *   The Next.js development server is not running or needs to be restarted.
    *   Browser caching.
*   **Solutions:**
    *   Ensure `npm run dev` is actively running in the frontend directory.
    *   Perform a hard refresh in your browser (Ctrl+F5 or Cmd+Shift+R).
    *   If the issue persists, stop the dev server, delete the `.next` folder, and restart.

### React Hydration Errors
*   **Symptom:** The console shows errors about mismatched HTML between server and client.
*   **Possible Causes:**
    *   Using browser-specific APIs (like `window` or `localStorage`) directly in the initial render without checking if it's the client side.
*   **Solutions:**
    *   Ensure browser APIs are only used within `useEffect` hooks or after checking `typeof window !== 'undefined'`.

## 3. Deployment Issues (Vercel / Railway)

### Vercel Build Fails
*   **Symptom:** The frontend deployment fails on Vercel during the build step.
*   **Possible Causes:**
    *   TypeScript compilation errors or ESLint warnings treated as errors.
    *   Missing environment variables in the Vercel project settings.
*   **Solutions:**
    *   Run `npm run build` and `npm run lint` locally to catch and fix errors before pushing.
    *   Ensure all necessary environment variables (e.g., `NEXT_PUBLIC_API_URL`) are configured in the Vercel dashboard.

### Railway/Render Service Unhealthy
*   **Symptom:** The backend deploys but the health check fails or it keeps restarting.
*   **Possible Causes:**
    *   Missing environment variables (e.g., `DATABASE_URL`, `SECRET_KEY`).
    *   Incorrect start command (should be `uvicorn app.main:app --host 0.0.0.0 --port $PORT`).
*   **Solutions:**
    *   Check the deployment logs on Railway/Render for the specific startup error.
    *   Verify all environment variables are correctly set in the platform's dashboard.