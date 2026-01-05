# API Reference - Complete Endpoints

## Base URL

```
http://localhost:8000/api/
```

## Authentication

All protected endpoints require JWT token or session authentication.

### Get JWT Token

```
POST /token/
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "password123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token

```
POST /token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Users Endpoints

### List Users

```
GET /users/
Parameters:
  - search: Search by username, name, title, location
  - ordering: -points, created_at, etc.
  - page: Page number (default: 1)

Response:
{
  "count": 100,
  "next": "http://.../users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "john_doe",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "title": "Junior Developer",
      "location": "San Francisco, CA",
      "bio": "...",
      "profile_picture": "https://...",
      "github_url": "https://github.com/johndoe",
      "linkedin_url": "https://linkedin.com/in/johndoe",
      "twitter_url": "https://twitter.com/johndoe",
      "website": "https://johndoe.com",
      "points": 1250,
      "is_mentor": true,
      "is_premium": false,
      "created_at": "2025-01-01T10:00:00Z",
      "updated_at": "2025-01-05T15:30:00Z",
      "skills": [...],
      "achievements": [...]
    }
  ]
}
```

### Get User Profile

```
GET /users/{id}/
GET /users/1/

Response: (single user object as above)
```

### Update User Profile

```
PUT /users/{id}/
PATCH /users/{id}/
Content-Type: application/json
Authorization: Bearer {token}

{
  "first_name": "John",
  "bio": "Updated bio",
  "title": "Senior Developer",
  "location": "New York, NY"
}

Response: (updated user object)
```

### Delete User Account

```
DELETE /users/{id}/
Authorization: Bearer {token}

Response: 204 No Content
```

### Get User Skills

```
GET /users/{id}/skills/

Response:
[
  {
    "id": 1,
    "skill": {
      "id": 1,
      "name": "Python",
      "category": "backend"
    },
    "proficiency_level": "advanced",
    "years_of_experience": 5,
    "endorsements_count": 12,
    "last_updated": "2025-01-05T15:30:00Z"
  }
]
```

### Get User Achievements

```
GET /users/{id}/achievements/

Response:
[
  {
    "id": 1,
    "achievement": {
      "id": 1,
      "name": "First Post",
      "description": "Create your first community post",
      "icon": "https://...",
      "rarity": "common",
      "points_awarded": 10
    },
    "earned_at": "2025-01-05T15:30:00Z"
  }
]
```

### Get User Statistics

```
GET /users/{id}/stats/

Response:
{
  "total_points": 1250,
  "total_skills": 8,
  "total_achievements": 5,
  "courses_completed": 3,
  "projects_completed": 2,
  "job_applications": 4,
  "community_posts": 12,
  "is_mentor": true
}
```

### Get Leaderboard

```
GET /users/leaderboard/

Response: Top 100 users by points (array of user objects)
```

---

## Skills Endpoints

### List Skills

```
GET /skills/
Parameters:
  - category: frontend, backend, devops, mobile, data-science, soft-skills
  - search: Search skill name

Response:
[
  {
    "id": 1,
    "name": "Python",
    "category": "backend",
    "description": "Python programming language"
  }
]
```

### Get My Skills

```
GET /user-skills/
Authorization: Bearer {token}

Response: (array of user skill objects)
```

### Add Skill

```
POST /user-skills/
Authorization: Bearer {token}
Content-Type: application/json

{
  "skill_id": 1,
  "proficiency_level": "intermediate",
  "years_of_experience": 3
}

Response:
{
  "id": 5,
  "skill": {...},
  "skill_id": 1,
  "proficiency_level": "intermediate",
  "years_of_experience": 3,
  "endorsements_count": 0
}
```

### Update Skill

```
PUT /user-skills/{id}/
PATCH /user-skills/{id}/
Authorization: Bearer {token}

{
  "proficiency_level": "advanced",
  "years_of_experience": 5
}
```

### Endorse Skill

```
POST /user-skills/{id}/endorse/
Authorization: Bearer {token}

Response:
{
  "id": 5,
  "skill": {...},
  "proficiency_level": "advanced",
  "endorsements_count": 13,  # Incremented
  "years_of_experience": 5
}
```

### Get Skill Gaps

```
GET /user-skills/gaps/
Authorization: Bearer {token}

Response: (array of recommended skills to learn)
```

---

## Resume Endpoints

### List My Resumes

```
GET /resumes/
Authorization: Bearer {token}

Response:
[
  {
    "id": 1,
    "user": {...},
    "file": "https://media.../resumes/resume_john.pdf",
    "file_type": "pdf",
    "extracted_text": "John Doe...",
    "extracted_skills": {...},
    "skill_gaps": [...],
    "experience_level": "mid-level",
    "skill_score": 85,
    "total_score": 78,
    "uploaded_at": "2025-01-05T15:30:00Z",
    "analyzed_at": "2025-01-05T15:31:00Z"
  }
]
```

### Upload Resume

```
POST /resumes/
Authorization: Bearer {token}
Content-Type: multipart/form-data

{
  "file": <binary file>,
  "file_type": "pdf"
}

Response: (resume object with analysis results)
```

### Get Resume Analysis

```
GET /resumes/{id}/analysis/
Authorization: Bearer {token}

Response:
{
  "skills": {
    "python": {"confidence": 95},
    "django": {"confidence": 90},
    ...
  },
  "skill_gaps": [
    "Kubernetes",
    "Docker",
    "AWS"
  ],
  "experience_level": "mid-level",
  "skill_score": 85,
  "total_score": 78,
  "analyzed_at": "2025-01-05T15:31:00Z"
}
```

---

## Courses Endpoints

### List Courses

```
GET /courses/
Parameters:
  - difficulty: beginner, intermediate, advanced
  - category: Web Development, Data Science, etc.
  - search: Search title or description
  - ordering: -rating, duration_hours, created_at

Response:
[
  {
    "id": 1,
    "title": "Python Basics",
    "description": "Learn Python from scratch",
    "difficulty": "beginner",
    "category": "Backend",
    "duration_hours": 20,
    "instructor": 5,
    "instructor_name": "John Smith",
    "thumbnail": "https://...",
    "total_students": 350,
    "rating": 4.8,
    "modules": [...],
    "created_at": "2024-12-01T10:00:00Z",
    "updated_at": "2025-01-05T15:30:00Z"
  }
]
```

### Get Course Details

```
GET /courses/{id}/
```

### Get Course Modules

```
GET /courses/{id}/modules/

Response:
[
  {
    "id": 1,
    "course": 1,
    "title": "Introduction to Python",
    "description": "...",
    "content_type": "video",
    "order": 1,
    "content": "...",
    "video_url": "https://youtube.com/...",
    "duration_minutes": 45,
    "created_at": "2024-12-01T10:00:00Z"
  }
]
```

### Enroll in Course

```
POST /courses/{id}/enroll/
Authorization: Bearer {token}

Response:
{
  "id": 1,
  "course": {...},
  "status": "in_progress",
  "progress_percentage": 0,
  "modules_completed": 0,
  "started_at": "2025-01-05T15:30:00Z"
}
```

### Get My Course Progress

```
GET /course-progress/
Authorization: Bearer {token}

Response: (array of user course progress objects)
```

### Mark Module Complete

```
POST /course-progress/{id}/mark_module_complete/
Authorization: Bearer {token}
Content-Type: application/json

{
  "module_id": 5
}

Response:
{
  "id": 1,
  "course": {...},
  "status": "in_progress",
  "progress_percentage": 25,  # Updated
  "modules_completed": 1,     # Incremented
  "started_at": "2025-01-05T15:30:00Z"
}
```

---

## Projects Endpoints

### List Projects

```
GET /projects/
Parameters:
  - difficulty: beginner, intermediate, advanced
  - search: Search title or description

Response:
[
  {
    "id": 1,
    "title": "Build a Todo App",
    "description": "Create a full-stack todo application",
    "requirements": "HTML, CSS, JavaScript, React",
    "difficulty": "intermediate",
    "required_skills": [...],
    "estimated_hours": 12,
    "total_submissions": 45,
    "average_rating": 4.5,
    "created_at": "2024-12-01T10:00:00Z"
  }
]
```

### Start Project

```
POST /projects/{id}/start/
Authorization: Bearer {token}

Response:
{
  "id": 1,
  "user": {...},
  "project": {...},
  "status": "in_progress",
  "submission_url": "",
  "submission_notes": "",
  "rating": null,
  "feedback": "",
  "started_at": "2025-01-05T15:30:00Z"
}
```

### Submit Project

```
POST /project-progress/{id}/submit/
Authorization: Bearer {token}
Content-Type: application/json

{
  "submission_url": "https://github.com/user/todo-app",
  "submission_notes": "Added additional features like dark mode"
}

Response:
{
  "id": 1,
  "status": "submitted",
  "submission_url": "https://...",
  "submission_notes": "...",
  "submitted_at": "2025-01-05T15:45:00Z"
}
```

### Get Project Leaderboard

```
GET /projects/{id}/leaderboard/

Response: (top 50 project submissions with highest ratings)
```

---

## Job Endpoints

### List Jobs

```
GET /jobs/
Parameters:
  - location: City name
  - job_type: full-time, part-time, contract, internship
  - experience_level: entry, junior, mid, senior
  - salary_min: Minimum salary
  - salary_max: Maximum salary
  - search: Search title, company, description, location

Response:
[
  {
    "id": 1,
    "title": "Senior Python Developer",
    "description": "...",
    "company_name": "TechCorp",
    "company_logo": "https://...",
    "location": "San Francisco, CA",
    "job_type": "full-time",
    "experience_level": "senior",
    "required_skills": [...],
    "salary_min": 120000,
    "salary_max": 180000,
    "application_url": "https://techdocs.com/careers/job/123",
    "total_applications": 45,
    "posted_at": "2025-01-01T10:00:00Z",
    "deadline": "2025-02-01T23:59:59Z"
  }
]
```

### Get Matching Jobs

```
GET /jobs/matching/
Authorization: Bearer {token}

Response: (jobs matching user's skills)
```

### Apply for Job

```
POST /jobs/{id}/apply/
Authorization: Bearer {token}
Content-Type: application/json

{
  "cover_letter": "I am very interested in this position..."
}

Response:
{
  "id": 1,
  "user": {...},
  "job": {...},
  "status": "applied",
  "cover_letter": "...",
  "applied_at": "2025-01-05T15:30:00Z"
}
```

### Get My Applications

```
GET /job-applications/
Authorization: Bearer {token}

Response: (array of user job applications)
```

### Update Application Status

```
POST /job-applications/{id}/update_status/
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "interview"
}

Response:
{
  "id": 1,
  "status": "interview",  # Updated
  "updated_at": "2025-01-05T16:00:00Z"
}
```

---

## Community Endpoints

### List Posts

```
GET /community/posts/
Parameters:
  - search: Search title, content, tags
  - ordering: -created_at, -likes_count, -comments_count

Response:
[
  {
    "id": 1,
    "author": {...},
    "title": "Tips for Learning Django",
    "content": "Here are some tips...",
    "tags": "django,python,backend",
    "likes_count": 25,
    "comments_count": 8,
    "comments": [...],
    "created_at": "2025-01-05T10:00:00Z",
    "updated_at": "2025-01-05T15:30:00Z"
  }
]
```

### Create Post

```
POST /community/posts/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "My First Post",
  "content": "This is the content of my post",
  "tags": "django,python,learning"
}

Response: (created post object)
```

### Like Post

```
POST /community/posts/{id}/like/
Authorization: Bearer {token}

Response:
{
  "likes_count": 26  # Incremented
}
```

### Get Post Comments

```
GET /community/posts/{id}/comments/

Response:
[
  {
    "id": 1,
    "post": 1,
    "author": {...},
    "content": "Great post!",
    "likes_count": 3,
    "created_at": "2025-01-05T11:00:00Z"
  }
]
```

### Add Comment

```
POST /community/comments/
Authorization: Bearer {token}
Content-Type: application/json

{
  "post": 1,
  "content": "Great post! Very helpful."
}

Response: (created comment object)
```

### Get Trending Posts

```
GET /community/posts/trending/

Response: (trending posts from last week)
```

---

## Mentor Endpoints

### List Mentors

```
GET /mentors/
Parameters:
  - hourly_rate_min: Minimum hourly rate
  - hourly_rate_max: Maximum hourly rate
  - rating_min: Minimum rating
  - years_min: Minimum years of experience
  - search: Search mentor name, specializations, bio

Response:
[
  {
    "id": 1,
    "user": {...},
    "specializations": "Python, Django, REST APIs",
    "hourly_rate": "75.00",
    "bio": "Senior developer with 10+ years experience",
    "total_mentees": 25,
    "rating": 4.9,
    "reviews_count": 18,
    "years_of_experience": 10,
    "availability_hours_per_week": 5,
    "sessions": [...],
    "created_at": "2024-12-01T10:00:00Z"
  }
]
```

### Get Mentor Reviews

```
GET /mentors/{id}/reviews/

Response: (completed mentoring sessions with ratings and feedback)
```

### Request Mentoring Session

```
POST /mentor-sessions/
Authorization: Bearer {token}
Content-Type: application/json

{
  "mentor": 1,
  "title": "Help with Django",
  "description": "I need help understanding Django ORM",
  "duration_minutes": 60
}

Response:
{
  "id": 1,
  "mentor": {...},
  "mentee": {...},
  "title": "Help with Django",
  "description": "...",
  "status": "pending",
  "duration_minutes": 60,
  "rating": null,
  "feedback": "",
  "requested_at": "2025-01-05T15:30:00Z"
}
```

### Schedule Session

```
POST /mentor-sessions/{id}/schedule/
Authorization: Bearer {token}
Content-Type: application/json

{
  "scheduled_date": "2025-01-10T14:00:00Z"
}

Response:
{
  "id": 1,
  "status": "scheduled",
  "scheduled_date": "2025-01-10T14:00:00Z"
}
```

### Complete Session

```
POST /mentor-sessions/{id}/complete/
Authorization: Bearer {token}
Content-Type: application/json

{
  "rating": 5,
  "feedback": "Great session! Very helpful."
}

Response:
{
  "id": 1,
  "status": "completed",
  "rating": 5,
  "feedback": "...",
  "completed_at": "2025-01-10T15:00:00Z"
}
```

---

## Achievement Endpoints

### List All Achievements

```
GET /achievements/
Parameters:
  - rarity: common, rare, epic, legendary

Response:
[
  {
    "id": 1,
    "name": "First Post",
    "description": "Create your first community post",
    "icon": "https://...",
    "rarity": "common",
    "points_awarded": 10,
    "created_at": "2024-12-01T10:00:00Z"
  }
]
```

### Get My Achievements

```
GET /user-achievements/
Authorization: Bearer {token}

Response: (user's earned achievements)
```

### Get User Achievements

```
GET /user-achievements/?user={id}

Response: (specific user's achievements)
```

---

## Error Responses

All endpoints return appropriate HTTP status codes:

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing/invalid authentication
- `403 Forbidden` - No permission
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Server Error` - Server error

### Error Response Format

```json
{
  "error": "Error message",
  "detail": "Detailed explanation",
  "field_errors": {
    "field_name": ["Error for this field"]
  }
}
```

---

## Rate Limiting

- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour

Rate limit info in response headers:

- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset`

---

## Pagination

Default: 10 items per page

Parameters:

- `page`: Page number (1-indexed)
- `page_size`: Items per page (1-100)

Response format:

```json
{
  "count": 100,
  "next": "http://.../resource/?page=2",
  "previous": null,
  "results": [...]
}
```
