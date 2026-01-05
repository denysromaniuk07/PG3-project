@echo off
REM Career Platform Backend - Quick Start Guide (Windows)

echo.
echo ============================================
echo 🚀 Career Platform Backend Setup (Windows)
echo ============================================
echo.

REM Step 1: Navigate to backend
echo 📍 Step 1: Checking current directory...
echo ✅ In: %CD%
echo.

REM Step 2: Create virtual environment (if not exists)
if not exist "venv" (
    echo 📍 Step 2: Creating Python virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)
echo.

REM Step 3: Activate virtual environment
echo 📍 Step 3: Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated
echo.

REM Step 4: Install requirements
echo 📍 Step 4: Installing dependencies...
pip install -r requirements.txt
echo ✅ Dependencies installed
echo.

REM Step 5: Run migrations
echo 📍 Step 5: Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo ✅ Migrations completed
echo.

REM Step 6: Create superuser
echo 📍 Step 6: Creating superuser...
echo   Note: Skip if already exists
python manage.py createsuperuser --noinput --username admin --email admin@example.com
echo ✅ Superuser ready
echo.

REM Step 7: Collect static files
echo 📍 Step 7: Collecting static files...
python manage.py collectstatic --noinput
echo ✅ Static files collected
echo.

echo.
echo 🎉 Setup Complete!
echo.
echo 📌 Next Steps:
echo   1. Start development server: python manage.py runserver
echo   2. Access admin: http://localhost:8000/admin/
echo   3. Browse API: http://localhost:8000/api/
echo   4. Login with username: admin (password set during creation)
echo.
echo 📝 To activate virtual environment in future:
echo   - Run: venv\Scripts\activate.bat
echo.
pause
