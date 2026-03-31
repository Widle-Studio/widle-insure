#!/bin/bash
# Run database migrations automatically on Vercel deployment
set -e

echo "🔄 Running database migrations..."

cd backend

# Install dependencies if needed
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run migrations
echo "📦 Running Alembic migrations..."
alembic upgrade head

# Seed initial admin user (only if doesn't exist)
echo "👤 Creating admin user..."
python scripts/create_admin.py

echo "✅ Database setup complete!"
