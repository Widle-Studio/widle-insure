FROM python:3.12-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency resolution and installation
RUN pip install uv

WORKDIR /app

# Copy the pyproject.toml and uv.lock from the root
# Since the context will likely be the project root
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# We use system python to install the dependencies into the venv
RUN uv pip install --system --no-cache -r pyproject.toml

# Now copy the backend code
COPY backend /app/backend

# Create the final lean image
FROM python:3.12-slim

# Install runtime system dependencies for OpenCV/YOLO
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app/backend:$PYTHONPATH"

# Copy the application
COPY --from=builder /app/backend /app/backend

# Expose the API port
EXPOSE 8000

# Default command runs the API, but can be overridden for Celery
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
