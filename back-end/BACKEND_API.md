# Career Platform - Backend API

A comprehensive Django REST Framework API powering a career development platform with 12+ major features.

## ✨ Features Implemented

### 1. User Management & Authentication

- Extended user profiles with career fields (title, location, bio, social links)
- JWT + Session authentication (djangorestframework-simplejwt)
- User statistics and global leaderboards
- Points/Gamification system

### 2. Resume Analysis

- PDF, DOCX, TXT file parsing
- ML-powered skill extraction with confidence scoring
- Experience level assessment (Entry → Senior)
- Skill gap analysis with recommendations

### 3. Skills Management

- Skill proficiency tracking (Beginner → Expert)
- Skill endorsements from peers
- Automatic skill gap recommendations
- Category-based skill organization

### 4. Learning System

- Courses with multiple modules
- Content types: Video, Text, Quiz, Exercise, Resource
- Progress tracking per course & module
- Completion percentage calculation
- Instructor assignment

### 5. Projects System

- Hands-on coding projects with requirements
- Difficulty levels (Beginner → Advanced)
- Project submissions with GitHub/demo links
- Rating & feedback system
- Leaderboards

### 6. Job Opportunities

- Job listings with required skills
- Smart skill-based matching
- Application tracking & status updates
- Salary ranges and job types
- Experience level requirements

### 7. Community & Discussion

- Posts, comments, likes
- Tagging/categorization system
- Trending topics algorithm
- User-generated content moderation
- Comment threads

### 8. Mentorship System

- Mentor profiles with specializations
- Mentor discovery & filtering
- Session scheduling & management
- Rating & review system
- Availability tracking

### 9. Achievements & Gamification

- Badge/Achievement system
- Rarity levels (Common → Legendary)
- Points per achievement
- User achievement tracking
- Global achievement leaderboards

### 10. Additional Features

- Advanced filtering & search
- Pagination (10 items per page)
- Rate limiting (100/hour anon, 1000/hour auth)
- CORS enabled for React frontend
- Media files serving
- Django admin interface

---

## 📦 Project Structure

```
back-end/
├── manage.py
├── requirements.txt
├── db.sqlite3
│
├── backend/                    # Django project settings
│   ├── __init__.py
│   ├── settings.py            # DRF, JWT, CORS, Database config
│   ├── urls.py                # Main URL router
│   ├── asgi.py
│   └── wsgi.py
│
├── api/                        # Main API app
│   ├── __init__.py
│   ├── models.py              # 15 models (User, Course, Job, etc.)
│   ├── serializers.py         # 17 serializers with nested relationships
│   ├── views_new.py           # 13 ViewSets with 40+ endpoints
│   ├── urls.py                # API routing
│   ├── permissions.py         # Custom permission classes
│   ├── filters.py             # FilterSets for advanced search
│   ├── admin.py               # Django admin configuration
│   ├── ml_utils.py            # Resume analysis ML utilities
│   ├── migrations/            # Database migrations
│   └── __pycache__/
│
├── core/                       # Reusable components
│   ├── __init__.py
│   ├── models.py              # Base model classes (TimeStamped, Ratable, etc.)
│   ├── mixins.py              # ViewSet mixins (Owner, Like, BulkAction, etc.)
│   ├── validators.py          # Custom validators (Email, File, Score, etc.)
│   └── __pycache__/
│
├── services/                   # Business logic services
│   ├── __init__.py
│   ├── resume_service.py      # Resume processing
│   ├── skill_service.py       # Skill recommendations
│   ├── recommendation_service.py  # Job/Course recommendations
│   ├── achievement_service.py # Badge/achievement logic
│   ├── analytics_service.py   # User statistics
│   └── notification_service.py
│
├── tasks/                      # Async tasks (Celery)
│   ├── __init__.py
│   ├── celery.py             # Celery configuration
│   ├── resume_tasks.py       # Async resume analysis
│   ├── email_tasks.py        # Email notifications
│   └── recommendation_tasks.py
│
├── middleware/                 # Custom middleware
│   ├── __init__.py
│   ├── auth_middleware.py
│   └── error_handler.py
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── constants.py           # App constants
│   ├── decorators.py          # Custom decorators
│   └── helpers.py             # Helper functions
│
└── media/                      # User uploads
    ├── avatars/
    ├── resumes/
    ├── courses/
    ├── projects/
    ├── achievements/
    └── company_logos/
```

---

## 🔌 API Endpoints

### Authentication

```
POST   /api/token/              - Get JWT token
POST   /api/token/refresh/      - Refresh JWT token
```

### Users

```
GET    /api/users/              - List all users
POST   /api/users/              - Create user
GET    /api/users/{id}/         - Get user profile
PUT    /api/users/{id}/         - Update profile
GET    /api/users/{id}/skills/  - Get user skills
GET    /api/users/{id}/achievements/  - Get achievements
GET    /api/users/{id}/stats/   - Get user statistics
GET    /api/users/leaderboard/  - Top users by points
```

### Skills

```
GET    /api/skills/             - List all skills
GET    /api/user-skills/        - My skills
POST   /api/user-skills/        - Add skill
PUT    /api/user-skills/{id}/   - Update skill
DELETE /api/user-skills/{id}/   - Remove skill
POST   /api/user-skills/{id}/endorse/  - Endorse skill
GET    /api/user-skills/gaps/   - Skill gaps
```

### Resume

```
GET    /api/resumes/            - My resumes
POST   /api/resumes/            - Upload resume
GET    /api/resumes/{id}/       - Get resume
GET    /api/resumes/{id}/analysis/  - Get analysis
DELETE /api/resumes/{id}/       - Delete resume
```

### Courses

```
GET    /api/courses/            - List courses (with filters)
GET    /api/courses/{id}/       - Get course details
GET    /api/courses/{id}/modules/  - Get modules
POST   /api/courses/{id}/enroll/    - Enroll in course
GET    /api/courses/{id}/progress/  - Get progress
GET    /api/course-progress/    - My courses
POST   /api/course-progress/{id}/mark_module_complete/
```

### Projects

```
GET    /api/projects/           - List projects (with filters)
GET    /api/projects/{id}/      - Get project details
POST   /api/projects/{id}/start/ - Start project
GET    /api/project-progress/   - My projects
POST   /api/project-progress/{id}/submit/  - Submit project
GET    /api/projects/{id}/leaderboard/  - Project leaderboard
```

### Jobs

```
GET    /api/jobs/               - List jobs (with advanced filters)
GET    /api/jobs/{id}/          - Get job details
GET    /api/jobs/matching/      - Recommended jobs
POST   /api/jobs/{id}/apply/    - Apply for job
GET    /api/job-applications/   - My applications
PUT    /api/job-applications/{id}/update_status/  - Update status
```

### Community

```
GET    /api/community/posts/    - List posts
POST   /api/community/posts/    - Create post
GET    /api/community/posts/{id}/  - Get post
PUT    /api/community/posts/{id}/  - Update post
DELETE /api/community/posts/{id}/  - Delete post
POST   /api/community/posts/{id}/like/  - Like post
GET    /api/community/posts/{id}/comments/  - Get comments
POST   /api/community/comments/ - Add comment
GET    /api/community/posts/trending/  - Trending
```

### Mentors

```
GET    /api/mentors/            - List mentors (with filters)
GET    /api/mentors/{id}/       - Get mentor profile
GET    /api/mentors/{id}/reviews/  - Mentor reviews
GET    /api/mentor-sessions/    - My sessions
POST   /api/mentor-sessions/    - Request session
POST   /api/mentor-sessions/{id}/schedule/  - Schedule session
POST   /api/mentor-sessions/{id}/complete/  - Complete session
```

### Achievements

```
GET    /api/achievements/       - All achievements
GET    /api/user-achievements/  - My achievements
GET    /api/user-achievements/?user={id}/  - User achievements
```

---

## 🔐 Authentication & Permissions

### Authentication Methods

- **JWT (JSON Web Tokens)** - For mobile/SPA apps
- **Session Authentication** - For browser-based clients

### Permission Classes

- `IsAuthenticated` - Requires logged-in user
- `IsOwner` - User can modify their own objects
- `IsAuthorOrReadOnly` - Author can edit, others read-only
- `IsMentor` - Mentor-only actions
- `AllowAny` - Public endpoints

---

## 🔍 Filtering & Search

### Job Opportunities

- Filter by: location, job_type, experience_level, salary_min, salary_max
- Search: title, company_name, description, location

### Courses

- Filter by: difficulty, category
- Search: title, description, category
- Sort by: created_at, rating, duration_hours

### Mentors

- Filter by: hourly_rate_min, hourly_rate_max, rating_min, years_min
- Search: name, specializations, bio

---

## 📊 Database Models

### Core Models

1. **User** - Extended with career fields
2. **Skill** & **UserSkill** - Skill management
3. **Resume** - Resume with ML analysis
4. **Course**, **CourseModule**, **UserCourseProgress** - Learning
5. **Project**, **UserProjectProgress** - Projects
6. **JobOpportunity**, **JobApplication** - Jobs
7. **CommunityPost**, **Comment** - Community
8. **Mentor**, **MentorSession** - Mentorship
9. **Achievement**, **UserAchievement** - Gamification

---

## 🛠️ Tech Stack

- **Framework**: Django 5.2.9
- **API**: Django REST Framework 3.16.1
- **Authentication**: djangorestframework-simplejwt 5.3.2
- **Filtering**: django-filter 24.1
- **Database**: SQLite (development), PostgreSQL (production)
- **ML**: scikit-learn, pandas, numpy
- **File Processing**: PyPDF2, python-docx
- **Task Queue**: Celery + Redis
- **Caching**: Redis
- **Images**: Pillow
- **Testing**: pytest, pytest-django

---

## ⚙️ Configuration

### Settings (`backend/settings.py`)

- REST Framework defaults (authentication, permissions, pagination)
- JWT configuration
- CORS for React frontend (localhost:3000)
- Database configuration
- Media files serving
- Rate limiting

### Environment Setup

```bash
cd back-end

# Install dependencies
pip install -r requirements.txt

# Create migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

## 📝 Core Module

The `core/` module provides reusable components:

### Base Models

- `TimeStampedModel` - Auto timestamps
- `SoftDeleteModel` - Soft delete capability
- `StatusModel` - Status tracking
- `RatableModel` - Rating system
- `CountableModel` - View/like counting

### ViewSet Mixins

- `OwnerFilterMixin` - Filter by owner
- `CreateUserMixin` - Auto set user on create
- `LikeDislikeMixin` - Like/unlike actions
- `BulkActionMixin` - Bulk operations
- `SearchFilterMixin` - Advanced search
- `ExportMixin` - CSV/JSON export
- `SoftDeleteMixin` - Soft delete actions

### Validators

- `URLValidator` - URL validation
- `SkillNameValidator` - Skill name validation
- `UsernameValidator` - Username rules
- `FileTypeValidator` - File type checking
- `FileSizeValidator` - File size limits
- `DateRangeValidator` - Date range validation
- And 6 more custom validators

---

## 🚀 Deployment

### Local Development

```bash
python manage.py runserver
```

### Production

```bash
# Collect static files
python manage.py collectstatic

# Run with gunicorn
gunicorn backend.wsgi:application
```

### Using Docker

```bash
docker build -t career-api .
docker run -p 8000:8000 career-api
```

---

## 📖 Admin Interface

Access Django admin at `/admin/` with superuser credentials.

All models are registered with:

- Custom list displays
- Smart filtering
- Search fields
- Proper permissions

---

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Submit a pull request

---

## 📄 License

This project is part of the Career Platform initiative.
