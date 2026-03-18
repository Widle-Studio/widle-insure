# API Documentation

The AI-Automated Auto Insurance Claims Platform utilizes FastAPI for its backend, which automatically generates interactive API documentation.

## Accessing the Documentation

Once the backend server is running locally, you can access the automatically generated API documentation in two formats:

1. **Swagger UI (Interactive):**
   - URL: `http://localhost:8000/docs`
   - Description: This interface allows you to explore the API endpoints, view their expected request/response schemas, and interactively test them directly from your browser.

2. **ReDoc (Alternative View):**
   - URL: `http://localhost:8000/redoc`
   - Description: A more static, clean documentation view that is excellent for reading API specifications.

## OpenAPI Schema

FastAPI uses the OpenAPI standard (formerly Swagger) to define the API. The raw OpenAPI JSON schema is available at:
- `http://localhost:8000/openapi.json`

## Authentication

Most endpoints (except for public ones like health checks and basic FNOL submission) require authentication.
- The platform uses JWT (JSON Web Tokens) for authentication.
- In the Swagger UI (`/docs`), click the **"Authorize"** button at the top right to provide your Bearer token.
- Once authorized, subsequent API requests made through the UI will automatically include the token in the `Authorization` header.

## Key API Modules

- **Claims (`/api/v1/claims`)**: Endpoints for submitting First Notice of Loss (FNOL) forms and uploading damage photos.
- **Admin (`/api/v1/admin`)**: Protected endpoints for claims management, review, approval/rejection, and analytics.
- **Policies (`/api/v1/policies`)**: Endpoints for policy lookup and validation (mocked for Alpha).
- **Payouts (`/api/v1/claims/{id}/payout`)**: Endpoints for initiating Stripe payouts for approved claims.
