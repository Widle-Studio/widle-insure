import logging

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.v1.endpoints import claims, payments, policies
from app.api.v1.endpoints.admin import auth as admin_auth
from app.api.v1.endpoints.admin import claims as admin_claims
from app.api.v1.endpoints.health import router as health_router
from app.core.config import settings
from app.core.log_config import setup_logging
from app.core.rate_limit import limiter

# Configure logging on startup
setup_logging()

# Initialize Sentry error logging
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        enable_tracing=True,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[
            StarletteIntegration(transaction_style="endpoint"),
            FastApiIntegration(transaction_style="endpoint"),
        ],
    )

logger = logging.getLogger(__name__)

# Configure Rate Limiter
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Configure CORS based on environment settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Accept", "x-api-key"],
)

import time  # noqa: E402

from fastapi import Request  # noqa: E402


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} "
        f"- {response.status_code} - {process_time:.2f}s"
    )

    return response



@app.get("/")
async def root():
    """Root endpoint providing a welcome message."""
    return {"message": "Welcome to Widle Insure API"}



app.include_router(health_router, tags=["health"])
app.include_router(
    claims.router, prefix=f"{settings.API_V1_STR}/claims", tags=["claims"]
)
app.include_router(
    policies.router, prefix=f"{settings.API_V1_STR}/policies", tags=["policies"]
)
app.include_router(
    payments.router, prefix=f"{settings.API_V1_STR}/payments", tags=["payments"]
)

app.include_router(
    admin_auth.router, prefix=f"{settings.API_V1_STR}/admin/auth", tags=["admin-auth"]
)
app.include_router(
    admin_claims.router,
    prefix=f"{settings.API_V1_STR}/admin/claims",
    tags=["admin-claims"],
)
