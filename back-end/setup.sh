#!/bin/bash

# Career Platform Backend - Quick Start Guide

echo "🚀 Career Platform Backend Setup"
echo "=================================="
echo ""

# Step 1: Navigate to backend
echo "📍 Step 1: Navigating to backend directory..."
cd "$(dirname "$0")" || exit
echo "✅ In: $(pwd)"
echo ""

# Step 2: Create virtual environment (if not exists)
if [ ! -d "venv" ]; then
    echo "📍 Step 2: Creating Python virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Step 3: Activate virtual environment
echo "📍 Step 3: Activating virtual environment..."
if [ -f "venv/Scripts/activate" ]; then
    # Windows
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    # macOS/Linux
    source venv/bin/activate
fi
echo "✅ Virtual environment activated"
echo ""

# Step 4: Install requirements
echo "📍 Step 4: Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Step 5: Run migrations
echo "📍 Step 5: Running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo "✅ Migrations completed"
echo ""

# Step 6: Create superuser
echo "📍 Step 6: Creating superuser..."
echo "  Note: Skip if already exists"
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true
echo "✅ Superuser ready (or already exists)"
echo ""

# Step 7: Collect static files
echo "📍 Step 7: Collecting static files..."
python manage.py collectstatic --noinput
echo "✅ Static files collected"
echo ""

echo "🎉 Setup Complete!"
echo ""
echo "📌 Next Steps:"
echo "  1. Start development server: python manage.py runserver"
echo "  2. Access admin: http://localhost:8000/admin/"
echo "  3. Browse API: http://localhost:8000/api/"
echo "  4. Login with credentials: admin / (set during creation)"
echo ""
