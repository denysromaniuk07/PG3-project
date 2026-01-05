# AI Career Platform Backend - Complete Architecture Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Core Components](#core-components)
6. [Data Models](#data-models)
7. [Authentication & Security](#authentication--security)
8. [API Layer](#api-layer)
9. [Business Logic (Services)](#business-logic-services)
10. [Asynchronous Processing (Tasks)](#asynchronous-processing-tasks)
11. [Middleware](#middleware)
12. [Data Flow](#data-flow)
13. [Deployment](#deployment)

---

## Introduction

The **AI Career Platform Backend** is a Django REST Framework application that powers a comprehensive career development platform. It provides:

- **User Management**: Profiles, skills, achievements, and gamification
- **Learning**: Courses, modules, progress tracking
- **Job Matching**: Job board with intelligent recommendations
- **Mentorship**: Mentor connections and session management
- **Community**: Discussion forums, networking
- **Resume Analysis**: ML-powered skill extraction and gap analysis
- **Notifications**: Real-time alerts and email notifications
- **Analytics**: Comprehensive user and platform metrics

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend                           │
│              (Runs on localhost:3000)                        │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         │
┌─────────────────────────▼────────────────────────────────────┐
│                                                              │
│                   NGINX / Web Server                         │
│                  (Reverse Proxy)                             │
│                                                              │
└────────────────────────┬────────────────────────────────────┘
                         │
┌─────────────────────────▼────────────────────────────────────┐
│                                                              │
│              Django REST Framework Server                    │
│                  (Port 8000)                                 │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            Middleware Stack                         │   │
│  │  • Authentication (JWT, Session)                   │   │
│  │  • Error Handling & Security                       │   │
│  │  • Rate Limiting & Throttling                      │   │
│  │  • Analytics & Logging                             │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────▼───────────────────────────────┐   │
│  │            API Layer (ViewSets)                      │   │
│  │  • Users, Skills, Resume, Courses, Projects, Jobs  │   │
│  │  • Community, Mentoring, Achievements              │   │
│  │  • Custom Actions & Filtering                      │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────▼───────────────────────────────┐   │
│  │         Business Logic (Services)                    │   │
│  │  • ResumeService (ML analysis)                      │   │
│  │  • SkillService (Skill management)                  │   │
│  │  • AchievementService (Gamification)                │   │
│  │  • RecommendationService (Personalization)          │   │
│  │  • NotificationService (Alerts)                     │   │
│  │  • AnalyticsService (Metrics)                       │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────▼───────────────────────────────┐   │
│  │         Core Module (Reusable Components)            │   │
│  │  • Base Models (TimeStamped, SoftDelete, etc)       │   │
│  │  • Mixins (OwnerFilter, LikeDislike, etc)           │   │
│  │  • Validators (Custom field validation)             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼────┐      ┌────▼────┐     ┌────▼────┐
   │ Database │      │  Cache  │     │  Redis  │
   │(SQLite/ │      │  Layer  │     │ (Celery)│
   │PostgreSQL)      │ (Django)│     │         │
   └─────────┘      └─────────┘     └────┬────┘
                                          │
                                    ┌─────▼──────┐
                                    │  Celery    │
                                    │  Workers   │
                                    │ (Async     │
                                    │  Jobs)     │
                                    └────────────┘
```

---

## Technology Stack

### Backend Framework

- **Django 5.2.9**: Web framework
- **Django REST Framework 3.16.1**: REST API
- **Celery 5.3.4**: Async task queue
- **Redis 5.0.1**: Caching & message broker

### Authentication & Security

- **djangorestframework-simplejwt 5.3.2**: JWT tokens
- **Django CORS Headers**: Cross-origin requests
- **Django Filter 24.1**: Advanced filtering

### Data & Processing

- **PostgreSQL / SQLite**: Database
- **pandas 2.1.4**: Data analysis
- **scikit-learn 1.3.2**: ML models
- **numpy 1.26.3**: Numerical computing
- **PyPDF2 3.0.1**: PDF processing
- **python-docx 0.8.11**: Word document processing
- **Pillow 10.1.0**: Image processing

### Testing & Development

- **pytest 7.4.3**: Testing framework
- **pytest-django 4.7.0**: Django test utilities
- **factory-boy 3.3.0**: Test data factories

---

## Project Structure

```
back-end/
├── api/                              # Main Django app
│   ├── models.py                     # 15 data models
│   ├── serializers.py                # 17 REST serializers
│   ├── views_new.py                  # 13 ViewSets (40+ endpoints)
│   ├── permissions.py                # 6 custom permission classes
│   ├── filters.py                    # 3 FilterSet classes
│   ├── urls.py                       # API routing
│   ├── admin.py                      # Django admin config
│   ├── ml_utils.py                   # ML analysis
│   └── migrations/                   # Database migrations
│
├── backend/                          # Project config
│   ├── settings.py                   # Django settings
│   ├── urls.py                       # Root URL config
│   ├── wsgi.py                       # Production server
│   └── asgi.py                       # WebSocket support
│
├── core/                             # Reusable components
│   ├── models.py                     # 5 abstract base models
│   ├── mixins.py                     # 9 ViewSet mixins
│   ├── validators.py                 # 13 custom validators
│   └── __init__.py                   # Exports
│
├── middleware/                       # Custom middleware
│   ├── auth_middleware.py            # JWT & session auth
│   ├── error_handler.py              # Exception handling
│   ├── analytics_middleware.py        # Activity tracking
│   ├── rate_limiting_middleware.py    # Rate limiting
│   └── __init__.py                   # Exports
│
├── services/                         # Business logic
│   ├── resume_service.py             # Resume processing
│   ├── skill_service.py              # Skill management
│   ├── achievement_service.py        # Gamification
│   ├── notification_service.py       # Notifications
│   ├── recommendation_service.py      # Recommendations
│   ├── analytics_service.py          # Analytics
│   └── __init__.py                   # Exports
│
├── tasks/                            # Async jobs
│   ├── celery.py                     # Celery config
│   ├── email_tasks.py                # Email notifications
│   ├── resume_tasks.py               # Resume processing
│   ├── recommendation_tasks.py        # Recommendations
│   ├── achievement_tasks.py          # Achievement checking
│   ├── notification_tasks.py         # Notification delivery
│   ├── analytics_tasks.py            # Analytics caching
│   └── __init__.py                   # Imports
│
├── utils/                            # Utilities
│   ├── constants.py                  # App constants
│   ├── decorators.py                 # Custom decorators
│   └── helpers.py                    # Helper functions
│
├── media/                            # File storage
│   ├── resumes/                      # Resume files
│   ├── avatars/                      # User profiles
│   ├── courses/                      # Course materials
│   └── projects/                     # Project files
│
├── logs/                             # Application logs
│   ├── django.log                    # General logs
│   └── errors.log                    # Error logs
│
├── requirements.txt                  # Python dependencies
├── manage.py                         # Django CLI
├── db.sqlite3                        # Development database
│
└── Documentation/
    ├── README.md                     # This file
    ├── API_REFERENCE.md              # Complete API docs
    ├── BACKEND_API.md                # Architecture overview
    ├── IMPLEMENTATION_SUMMARY.md     # Component summary
    ├── CORE_USAGE_GUIDE.md           # Core module guide
    ├── SERVICES_GUIDE.md             # Services guide
    ├── SERVICES_QUICK_REFERENCE.md   # Services reference
    ├── MIDDLEWARE_GUIDE.md           # Middleware docs
    ├── MIDDLEWARE_QUICK_REFERENCE.md # Middleware reference
    ├── TASKS_GUIDE.md                # Celery tasks docs
    ├── TASKS_QUICK_REFERENCE.md      # Tasks reference
    ├── setup.sh                      # Unix setup script
    └── setup.bat                     # Windows setup script
```

---

## Core Components

### 1. API Layer (RESTful Endpoints)

**What it does**: Exposes business logic through HTTP REST endpoints

**Components**:

- **ViewSets** (13 total): Handle CRUD operations + custom actions
- **Serializers** (17 total): Convert models to/from JSON
- **Permissions** (6 total): Control endpoint access
- **Filters** (3 total): Enable advanced querying

**Endpoints Structure**:

```
/api/users/                    # User management
/api/skills/                   # Skill operations
/api/resumes/                  # Resume upload & analysis
/api/courses/                  # Course enrollment
/api/projects/                 # Project submissions
/api/jobs/                     # Job applications
/api/community/posts/          # Discussion forums
/api/mentors/                  # Mentor connections
/api/achievements/             # Achievement tracking
```

**Example ViewSet**:

```python
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def skills(self, request, pk=None):
        # Return user's skills
        pass

    @action(detail=False)
    def leaderboard(self, request):
        # Return top users by points
        pass
```

### 2. Services Layer (Business Logic)

**What it does**: Contains complex business operations and data transformations

**Six Main Services**:

1. **ResumeService**

   - Uploads resume files (PDF/DOCX)
   - Extracts text using PyPDF2/python-docx
   - Runs ML analysis using scikit-learn
   - Syncs identified skills with user profile

2. **SkillService**

   - Manages user skills
   - Endorses skills
   - Identifies skill gaps
   - Tracks trending skills

3. **AchievementService**

   - Defines 10 achievements with unlock conditions
   - Awards points to users
   - Generates leaderboards
   - Tracks achievement progress

4. **NotificationService**

   - Creates notifications for events
   - Sends emails asynchronously
   - Tracks notification state
   - Cleans up old notifications

5. **RecommendationService**

   - Recommends jobs based on skills
   - Suggests courses for learning
   - Suggests mentors
   - Recommends connections

6. **AnalyticsService**
   - Tracks user activity
   - Generates platform metrics
   - Creates activity heatmaps
   - Reports skill demand

### 3. Middleware (Request/Response Processing)

**What it does**: Processes HTTP requests/responses at a global level

**Components**:

1. **Authentication Middleware**

   - Validates JWT tokens
   - Enriches requests with user context
   - Checks token blacklist

2. **Error Handling Middleware**

   - Catches exceptions
   - Adds security headers
   - Logs request/response

3. **Analytics Middleware**

   - Tracks API usage
   - Monitors response times
   - Records user activity

4. **Rate Limiting Middleware**
   - Limits requests per hour (100 anon, 1000 auth)
   - Limits burst requests (20/minute)
   - Whitelists internal IPs

### 4. Core Module (Reusable Components)

**What it does**: Provides reusable base classes and utilities

**Base Models** (5):

- `TimeStampedModel`: auto_now_add, auto_now fields
- `SoftDeleteModel`: is_deleted flag with restore
- `StatusModel`: status choices (active/inactive)
- `RatableModel`: rating system
- `CountableModel`: view/like counters

**Mixins** (9):

- `OwnerFilterMixin`: Filter by user/author
- `CreateUserMixin`: Auto-set user on create
- `LikeDislikeMixin`: Like/unlike actions
- `SearchFilterMixin`: Q-object search
- `SoftDeleteMixin`: Soft delete actions
- Plus 4 more...

**Validators** (13):

- URL validation
- Skill name validation
- Username validation
- File type/size checking
- Date range validation
- JSON schema validation
- Plus 6 more...

---

## Data Models

### User System (3 models)

**User**

```python
- username, email, password
- first_name, last_name
- profile_picture, bio
- title (job title)
- location, website
- social links (GitHub, LinkedIn, Twitter)
- points, is_mentor, is_premium
- created_at, updated_at
```

**Skill & UserSkill**

```python
Skill:
- name, category (backend, frontend, etc.)
- description

UserSkill:
- user, skill
- proficiency_level (beginner-expert)
- years_of_experience
- endorsements_count
```

### Learning System (3 models)

**Course**

```python
- title, description
- difficulty, category, duration_hours
- instructor (ForeignKey to User)
- rating, total_students
- required_skills (ManyToMany)
```

**CourseModule**

```python
- course, title
- content_type (video, text, quiz, exercise, resource)
- content, video_url, duration_minutes
- order
```

**UserCourseProgress**

```python
- user, course
- status (in_progress, completed, dropped)
- progress_percentage
- modules_completed, started_at, completed_at
```

### Project System (2 models)

**Project**

```python
- title, description
- difficulty, category
- requirements, estimated_hours
- total_submissions, average_rating
- required_skills (ManyToMany)
```

**UserProjectProgress**

```python
- user, project
- status (in_progress, submitted, completed)
- submission_url, submission_notes
- rating, feedback
- started_at, submitted_at
```

### Job System (2 models)

**JobOpportunity**

```python
- title, description, company_name, company_logo
- location, job_type (full-time, part-time, etc.)
- experience_level (entry, junior, mid, senior)
- required_skills (ManyToMany)
- salary_min, salary_max
- application_url, deadline
- status (active, closed)
```

**JobApplication**

```python
- user, job
- status (applied, interview, rejected, accepted)
- cover_letter
- applied_at, updated_at
```

### Resume System (1 model)

**Resume**

```python
- user, file (PDF/DOCX)
- file_type, extracted_text
- extracted_skills (JSON dict)
- skill_gaps (JSON array)
- experience_level
- skill_score (0-100)
- total_score (0-100)
- uploaded_at, analyzed_at
```

### Community System (2 models)

**CommunityPost**

```python
- author (ForeignKey to User)
- title, content, tags
- likes_count, comments_count
- created_at, updated_at
```

**Comment**

```python
- post, author
- content
- likes_count
- created_at, updated_at
```

### Mentorship System (2 models)

**Mentor**

```python
- user (OneToOne to User)
- specializations
- hourly_rate
- bio, rating, years_of_experience
- availability_hours_per_week
```

**MentorSession**

```python
- mentor, mentee
- title, description
- status (pending, scheduled, completed)
- duration_minutes
- scheduled_date
- rating, feedback
- requested_at, completed_at
```

### Gamification System (2 models)

**Achievement**

```python
- name, description
- icon, rarity (common, rare, epic, legendary)
- points_awarded, key (unique identifier)
- created_at
```

**UserAchievement**

```python
- user, achievement
- earned_at
```

---

## Authentication & Security

### JWT (JSON Web Tokens)

**Flow**:

1. User sends username + password to `/token/`
2. Server returns `access` and `refresh` tokens
3. Client includes `Authorization: Bearer <access_token>` in requests
4. Access tokens expire in 5 minutes
5. Use `refresh_token` to get new `access_token`

**Token Structure**:

```python
{
    "user_id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "iat": 1704456000,  # Issued at
    "exp": 1704456300   # Expires at
}
```

### Permissions

**Predefined Classes**:

- `IsAuthenticated`: User must be logged in
- `IsAuthenticatedOrReadOnly`: Anyone reads, only auth writes
- `IsOwner`: User owns the object
- `IsAuthorOrReadOnly`: Author edits, others read
- `IsMentor`: User must be a mentor

**Example**:

```python
class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    # Only authenticated users can access
    # Users can only access their own profile
```

### Security Headers

Middleware adds:

- `X-Frame-Options: DENY` - Prevents clickjacking
- `X-Content-Type-Options: nosniff` - MIME sniffing
- `X-XSS-Protection: 1; mode=block` - XSS protection
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Content-Security-Policy: ...`

---

## API Layer

### How Requests Flow Through API

```
HTTP Request
    │
    ├─ URL Router (urls.py)
    │   └─ Matches endpoint pattern
    │
    ├─ Middleware Stack
    │   ├─ Authentication (JWT validation)
    │   ├─ Error Handler (catches exceptions)
    │   └─ Rate Limiting (checks quota)
    │
    ├─ ViewSet Method
    │   ├─ Permission Check
    │   ├─ Deserialization (JSON → Python)
    │   ├─ Validation
    │   └─ Business Logic
    │
    ├─ Service Layer
    │   ├─ Complex operations
    │   ├─ Database interactions
    │   └─ External calls
    │
    ├─ Serialization (Python → JSON)
    │
    └─ HTTP Response
```

### Example: Resume Upload Endpoint

```python
# Request
POST /api/resumes/
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <binary PDF>
file_type: "pdf"

# ViewSet Method
def perform_create(self, serializer):
    resume = serializer.save(user=self.request.user)
    # Trigger async analysis
    analyze_resume_async.delay(resume.id)

# Service Layer
ResumeService.upload_and_analyze_resume(
    user=user,
    resume_file=file,
    file_type='pdf'
)

# Database Operations
Resume.objects.create(...)
extracted_text = extract_text_from_resume(...)
analysis_results = analyze_resume(extracted_text)
Resume.objects.update(...)
UserSkill.objects.create(...)

# Response
{
    "id": 1,
    "user": {...},
    "file": "https://...",
    "extracted_skills": {"Python": 0.95, "Django": 0.92},
    "skill_gaps": ["Kubernetes", "Docker"],
    "experience_level": "mid-level",
    "total_score": 78,
    "analyzed_at": "2025-01-05T15:31:00Z"
}
```

---

## Business Logic (Services)

### Service Architecture

**Principle**: Keep views thin, put logic in services

**Benefits**:

- Reusable across views, tasks, admin
- Testable in isolation
- Easier to modify
- Better organization

### Service Example: Skill Endorsement

```python
# In View
@action(detail=True, methods=['post'])
def endorse(self, request, pk=None):
    user_skill = self.get_object()
    SkillService.endorse_skill(
        endorser=request.user,
        user=user_skill.user,
        skill_id=user_skill.skill_id
    )
    return Response({'success': True})

# In Service
@staticmethod
def endorse_skill(endorser, user, skill_id):
    user_skill = UserSkill.objects.get(user=user, skill_id=skill_id)
    user_skill.endorsements_count += 1
    user_skill.save()

    # Award points
    user.points += 5
    user.save()

    # Check for achievements
    AchievementService.check_and_unlock_achievements(user)
```

---

## Asynchronous Processing (Tasks)

### Why Celery?

**Problem**: Long operations block HTTP response

- Resume analysis: 2-5 seconds
- Email sending: 1-3 seconds
- ML predictions: variable time

**Solution**: Queue async tasks

### Task Categories

**Email Tasks** (8 tasks)

- Welcome emails
- Achievement notifications
- Job match alerts
- Mentor requests
- Daily digests

**Resume Tasks** (4 tasks)

- Async ML analysis
- Text extraction
- Batch processing
- Cleanup old resumes

**Recommendation Tasks** (7 tasks)

- Job recommendations
- Course suggestions
- Mentor matching
- Skill recommendations
- Connection suggestions

**Achievement Tasks** (5 tasks)

- Achievement checking
- Unlocking
- Stats generation
- Milestone detection

**Notification Tasks** (7 tasks)

- Notification delivery
- Mention notifications
- Like/comment alerts
- Batch sending

**Analytics Tasks** (7 tasks)

- Platform stats caching
- User analytics
- Activity heatmaps
- Growth reports

### Celery Beat (Scheduler)

Runs tasks automatically:

| Task                             | Frequency | Purpose                      |
| -------------------------------- | --------- | ---------------------------- |
| `cache_platform_analytics`       | Hourly    | Cache expensive stats        |
| `check_all_user_achievements`    | Hourly    | Auto-unlock achievements     |
| `generate_daily_recommendations` | Daily     | Personalized recommendations |
| `cleanup_old_notifications`      | Daily     | Delete old notifications     |
| `send_daily_digest`              | Daily     | Email summaries              |

---

## Middleware

### Request Processing Pipeline

```
Incoming Request
    │
    ├─ SecurityMiddleware
    │   └─ HTTPS enforcement
    │
    ├─ CorsMiddleware
    │   └─ Cross-origin requests
    │
    ├─ SessionMiddleware
    │   └─ Session handling
    │
    ├─ JWTAuthenticationMiddleware (Custom)
    │   ├─ Extract token from header
    │   ├─ Validate signature
    │   └─ Set request.user
    │
    ├─ UserContextMiddleware (Custom)
    │   └─ Enrich with user data
    │
    ├─ TokenBlacklistMiddleware (Custom)
    │   └─ Check if token revoked
    │
    ├─ ExceptionHandlerMiddleware (Custom)
    │   └─ Catch exceptions
    │
    ├─ SecurityHeadersMiddleware (Custom)
    │   └─ Add security headers
    │
    ├─ RequestResponseLoggingMiddleware (Custom)
    │   └─ Log request/response
    │
    ├─ AnalyticsMiddleware (Custom)
    │   ├─ Track API usage
    │   └─ Measure response time
    │
    ├─ UserActivityMiddleware (Custom)
    │   └─ Record user activity
    │
    ├─ RateLimitMiddleware (Custom)
    │   ├─ Check hourly limit
    │   ├─ Check burst limit
    │   └─ Track requests
    │
    └─ View Processing
        └─ Handle request
```

### Rate Limiting Example

```
Anonymous user: 100 requests/hour
- Exceeded? Return 429 Too Many Requests

Authenticated user: 1000 requests/hour
- Exceeded? Return 429 Too Many Requests

Burst limit: 20 requests/minute
- Exceeded? Return 429 Too Many Requests

Response headers:
X-RateLimit-Limit-Hourly: 1000
X-RateLimit-Remaining-Hourly: 987
X-RateLimit-Reset-Hourly: 1641234567
```

---

## Data Flow

### Complete User Journey: From Registration to Recommendation

```
1. User Signs Up
   └─ POST /api/users/register/
      └─ Create User record
      └─ Send welcome email (async)
      └─ Check achievements (async)

2. User Adds Skills
   └─ POST /api/user-skills/
      └─ Create UserSkill record
      └─ Check achievements (async)

3. User Uploads Resume
   └─ POST /api/resumes/
      └─ Save file
      └─ Queue async analysis

4. Resume Analysis (Celery Task)
   └─ Extract text
   └─ Run ML analysis
   └─ Identify skills
   └─ Update resume record
   └─ Sync to UserSkill
   └─ Check achievements (async)
   └─ Send notification

5. User Gets Recommendations
   └─ GET /api/users/1/recommendations/
      └─ Call RecommendationService
      └─ Analyze user skills
      └─ Find skill gaps
      └─ Rank matching jobs/courses
      └─ Cache results
      └─ Return to user

6. User Applies for Job
   └─ POST /api/job-applications/
      └─ Create JobApplication
      └─ Check achievements (async)
      └─ Generate new recommendations (async)

7. Background Jobs (Celery Beat)
   └─ Hourly: Cache platform analytics
   └─ Daily: Generate recommendations for all users
   └─ Daily: Send email digests
```

### Achievement Unlock Flow

```
Action: User creates first post
   │
   ├─ ViewSet.perform_create()
   │   └─ Create CommunityPost
   │
   ├─ Trigger check_user_achievements (async)
   │   └─ achievement_tasks.check_user_achievements()
   │
   ├─ Service layer checks conditions
   │   └─ AchievementService.check_and_unlock_achievements()
   │
   ├─ Found unlockable achievement
   │   └─ AchievementService.unlock_achievement()
   │
   ├─ Update user points
   │   └─ user.points += achievement.points_awarded
   │
   ├─ Create notification
   │   └─ NotificationService.notify_achievement_unlocked()
   │
   ├─ Send email (async)
   │   └─ send_achievement_email.delay()
   │
   └─ Update leaderboard cache
       └─ cache.set('achievement_leaderboard', ...)
```

---

## Deployment

### Development Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database
python manage.py makemigrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Start Redis (in separate terminal)
redis-server

# 6. Start Celery worker (in separate terminal)
celery -A tasks worker -B -l info

# 7. Start Django server
python manage.py runserver
```

### Production Deployment

**Server Setup**:

```bash
# 1. Install on Ubuntu/Debian
sudo apt-get install python3-pip postgresql redis-server nginx

# 2. Setup database
sudo -u postgres createdb career_platform

# 3. Configure environment variables
export DATABASE_URL=postgres://user:pass@localhost/career_platform
export REDIS_URL=redis://localhost:6379/0
export SECRET_KEY=<generate_random_key>
export DEBUG=False
export ALLOWED_HOSTS=yourdomain.com

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Run migrations
python manage.py migrate

# 6. Start with Gunicorn
gunicorn backend.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --worker-class sync

# 7. Start Celery worker
celery -A tasks worker -l info -Q default

# 8. Start Celery Beat
celery -A tasks beat -l info
```

**Nginx Configuration**:

```nginx
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /path/to/static/;
    }

    location /media/ {
        alias /path/to/media/;
    }
}
```

---

## Summary: What Each Component Does

| Component          | Purpose                     | Technology                          |
| ------------------ | --------------------------- | ----------------------------------- |
| **API/ViewSets**   | HTTP endpoints              | Django REST Framework               |
| **Serializers**    | JSON conversion             | DRF Serializers                     |
| **Permissions**    | Access control              | DRF Permissions                     |
| **Services**       | Business logic              | Python Classes                      |
| **Models**         | Data structure              | Django ORM                          |
| **Middleware**     | Request/response processing | Django Middleware                   |
| **Tasks**          | Async processing            | Celery                              |
| **Core**           | Reusable components         | Abstract Models, Mixins, Validators |
| **Database**       | Data persistence            | PostgreSQL/SQLite                   |
| **Cache**          | Performance                 | Redis/Django Cache                  |
| **Authentication** | User verification           | JWT Tokens                          |

---

## Key Architecture Principles

### 1. **Separation of Concerns**

- Views handle HTTP
- Services handle business logic
- Models handle data
- Tasks handle async work

### 2. **DRY (Don't Repeat Yourself)**

- Base classes for common functionality
- Mixins for shared behavior
- Services for reusable logic

### 3. **SOLID Principles**

- Single Responsibility: Each class has one reason to change
- Open/Closed: Open for extension, closed for modification
- Liskov Substitution: Subclasses work where parent works
- Interface Segregation: Specific interfaces over general ones
- Dependency Inversion: Depend on abstractions, not implementations

### 4. **Performance**

- Async for long operations
- Caching for expensive queries
- Pagination for large datasets
- Database optimization (select_related, prefetch_related)

### 5. **Security**

- JWT tokens with expiration
- CORS restrictions
- Rate limiting
- Security headers
- Input validation
- SQL injection prevention (ORM)

---

## API Response Format

### Success Response

```json
{
    "id": 1,
    "data": {...},
    "status": 200
}
```

### Error Response

```json
{
  "error": "Validation Error",
  "detail": "One or more fields contain invalid values",
  "field_errors": {
    "email": ["Invalid email format"]
  },
  "status": 400
}
```

### Paginated Response

```json
{
    "count": 100,
    "next": "http://.../api/users/?page=2",
    "previous": null,
    "results": [...]
}
```

---

## Next Steps

1. **Read Component Guides**

   - [API_REFERENCE.md](API_REFERENCE.md) - Complete endpoint documentation
   - [SERVICES_GUIDE.md](SERVICES_GUIDE.md) - Service usage guide
   - [TASKS_GUIDE.md](TASKS_GUIDE.md) - Celery task documentation
   - [MIDDLEWARE_GUIDE.md](MIDDLEWARE_GUIDE.md) - Middleware details

2. **Setup Development Environment**

   - Follow [setup.sh](setup.sh) or [setup.bat](setup.bat)
   - Configure Redis
   - Start Celery worker

3. **Explore Code**

   - Review models in `api/models.py`
   - Study ViewSets in `api/views_new.py`
   - Check service implementations in `services/`

4. **Test APIs**

   - Use API_REFERENCE.md for endpoint examples
   - Test with curl, Postman, or REST client
   - Check Django admin at http://localhost:8000/admin/

5. **Monitor**
   - Check logs in `logs/` directory
   - Monitor Celery with Flower: `celery -A tasks flower`
   - Use Django admin for data management

---

## Support & Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Celery Documentation**: https://docs.celeryproject.org/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Redis**: https://redis.io/documentation

  GET /api/jobs/{id}/applicants/ - List applicants (admin)

7. Community & Discussion

   GET /api/community/posts/ - List community posts

   POST /api/community/posts/ - Create post

   GET /api/community/posts/{id}/ - Get post details

   PUT /api/community/posts/{id}/ - Update post

   DELETE /api/community/posts/{id}/ - Delete post

   POST /api/community/posts/{id}/like/ - Like post

   POST /api/community/posts/{id}/comments/ - Add comment

   GET /api/community/tags/ - List tags

   GET /api/community/trending/ - Get trending topics

8. Mentorship

   GET /api/mentors/ - List mentors

   GET /api/mentors/{id}/ - Get mentor profile

   POST /api/mentor-profile/ - Create mentor profile

   PUT /api/mentor-profile/{id}/ - Update mentor profile

   GET /api/mentor-profile/{id}/reviews/ - Get mentor reviews

   POST /api/mentee-sessions/ - Request mentoring session

   GET /api/mentee-sessions/ - List user sessions

   PUT /api/mentee-sessions/{id}/ - Update session status

9. Achievements & Gamification

   GET /api/achievements/ - List all achievements

   GET /api/user/achievements/ - Get user achievements

   POST /api/user/achievements/ - Award achievement

   GET /api/user/leaderboard/ - Global leaderboard

   GET /api/user/points/ - Get user points

   Database Schema Overview

   Core Models:

User - Extended with career fields (title, location, bio, social links, points)
UserSkill - User's skills with proficiency level and endorsements
Resume - Uploaded resumes with ML analysis results
Course - Learning courses with difficulty levels
CourseModule - Course sections with various content types
UserCourseProgress - Track course completion
Project - Coding projects with requirements
UserProjectProgress - Track project submissions
JobOpportunity - Job listings with skill requirements
JobApplication - Track applications and status
CommunityPost - Discussion posts with tags
Comment - Post comments and replies
Achievement - Badges and achievements
UserAchievement - User earned badges
Mentor - Mentor profiles and qualifications
Technology Recommendations
Backend Stack:

Framework: Django REST Framework (already in use)
Database: PostgreSQL (upgrade from SQLite for production)
Cache: Redis (for caching, sessions, task queue)
Task Queue: Celery (async resume analysis, notifications)
Search: Elasticsearch (for job/course/mentor search)
Auth: JWT + DRF Token Authentication
ML: Your existing ml_utils.py + scikit-learn for recommendations
Frontend Stack:

React with TailwindCSS (already in use)
React Router (already in use)
Axios for API calls
Context API or Redux for state management

This architecture supports all 12 features with clear separation of concerns, scalability, and maintainability. Would you like me to help implement any specific feature or refactor the code to follow this structure?
