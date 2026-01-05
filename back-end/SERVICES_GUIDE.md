# Services Documentation

## Overview

The services layer contains business logic that handles complex operations, data transformations, and interactions across multiple models. Each service is focused on a specific domain.

---

## Services Overview

### 1. ResumeService

Handles resume file uploads, text extraction, and ML-powered analysis.

**Key Methods:**

#### `upload_and_analyze_resume(user, resume_file, file_type='pdf')`

Upload and analyze a resume file.

```python
from services import ResumeService

resume = ResumeService.upload_and_analyze_resume(
    user=request.user,
    resume_file=request.FILES['resume'],
    file_type='pdf'
)
```

**Returns:** Resume object with analysis results

- `extracted_text`: Raw text from resume
- `extracted_skills`: Dict of {skill_name: confidence}
- `skill_gaps`: List of missing skills
- `experience_level`: Entry/Mid/Senior
- `skill_score`: 0-100
- `total_score`: 0-100

#### `get_resume_analysis(resume_id)`

Get detailed analysis results.

```python
analysis = ResumeService.get_resume_analysis(resume_id)
# Returns: {
#   'resume_id': 1,
#   'extracted_skills': {...},
#   'skill_gaps': [...],
#   'experience_level': 'mid-level',
#   'skill_score': 85,
#   'total_score': 78,
#   'analyzed_at': '2025-01-05T15:30:00Z'
# }
```

#### `compare_resumes(resume_id_1, resume_id_2)`

Compare two resumes.

```python
comparison = ResumeService.compare_resumes(resume_1_id, resume_2_id)
# Returns unique skills, common skills, and score differences
```

#### `delete_resume(resume_id)`

Delete a resume.

```python
ResumeService.delete_resume(resume_id)
```

---

### 2. SkillService

Manages user skills, endorsements, and skill-based recommendations.

**Key Methods:**

#### `add_skill_to_user(user, skill_id, proficiency_level, years_of_experience)`

Add a skill to user's profile.

```python
user_skill = SkillService.add_skill_to_user(
    user=request.user,
    skill_id=1,
    proficiency_level='advanced',
    years_of_experience=3
)
```

#### `remove_skill_from_user(user, skill_id)`

Remove a skill.

```python
SkillService.remove_skill_from_user(request.user, skill_id=1)
```

#### `endorse_skill(endorser, user, skill_id)`

Endorse another user's skill.

```python
user_skill = SkillService.endorse_skill(
    endorser=request.user,
    user=other_user,
    skill_id=1
)
# Awards 5 points to endorsed user
```

#### `get_skill_gaps(user)`

Get recommended skills to learn.

```python
gaps = SkillService.get_skill_gaps(request.user)
# Returns: [
#   {
#     'skill_id': 1,
#     'skill_name': 'Kubernetes',
#     'skill_category': 'devops',
#     'job_count': 45,
#     'reason': 'Required in 45 active job postings'
#   }
# ]
```

#### `get_trending_skills()`

Get trending skills platform-wide.

```python
trending = SkillService.get_trending_skills()
```

#### `get_skill_demand()`

Get in-demand skills based on job market.

```python
in_demand = SkillService.get_skill_demand()
# Returns top 20 skills by job demand
```

#### `batch_add_skills(user, skills_data)`

Add multiple skills in one transaction.

```python
skills = SkillService.batch_add_skills(
    user=request.user,
    skills_data=[
        {'skill_id': 1, 'proficiency_level': 'advanced', 'years_of_experience': 3},
        {'skill_id': 2, 'proficiency_level': 'intermediate', 'years_of_experience': 1},
    ]
)
```

---

### 3. AchievementService

Manages achievement unlocking and gamification.

**Key Methods:**

#### `check_and_unlock_achievements(user)`

Check and unlock any new achievements.

```python
AchievementService.check_and_unlock_achievements(request.user)
```

**Automatic Achievements:**

- `first_post`: 10 points
- `first_resume`: 15 points
- `first_course`: 20 points
- `course_completion`: 50 points
- `skill_endorser`: 25 points
- `mentor`: 100 points
- `job_seeker`: 30 points
- `community_leader`: 75 points
- `skill_master`: 60 points
- `legend`: 250 points

#### `unlock_achievement(user, achievement_key)`

Manually unlock an achievement.

```python
AchievementService.unlock_achievement(user, 'first_post')
```

#### `get_user_achievements(user)`

Get user's earned achievements.

```python
achievements = AchievementService.get_user_achievements(request.user)
```

#### `get_achievement_progress(user)`

Get progress towards locked achievements.

```python
progress = AchievementService.get_achievement_progress(request.user)
# Returns achievements with progress percentage
```

#### `get_leaderboard(limit=100)`

Get achievement leaderboard.

```python
leaderboard = AchievementService.get_leaderboard(limit=50)
# Returns top 50 users by points
```

---

### 4. NotificationService

Handles user notifications and alerts.

**Key Methods:**

#### `create_notification(user, notification_type, title, message, related_user)`

Create a notification.

```python
notification = NotificationService.create_notification(
    user=recipient_user,
    notification_type='achievement',
    title='Achievement Unlocked!',
    message='You earned the "First Post" achievement',
    related_user=None
)
```

**Notification Types:**

- `achievement` - Achievement unlocked
- `mention` - User mentioned
- `like` - Post liked
- `comment` - Comment added
- `job_match` - Job match found
- `mentor_request` - Mentor request
- `system` - System alert

#### `notify_achievement_unlocked(user, achievement)`

Notify achievement unlock.

```python
AchievementService.unlock_achievement(user, 'first_post')
NotificationService.notify_achievement_unlocked(user, achievement)
```

#### `notify_job_match(user, job)`

Notify job match.

```python
NotificationService.notify_job_match(user, job_opportunity)
```

#### `notify_mentor_request(mentor, mentee, session)`

Notify mentor about new request.

```python
NotificationService.notify_mentor_request(mentor, mentee, session)
```

#### `get_user_notifications(user, unread_only=False, limit=20)`

Get user's notifications.

```python
notifications = NotificationService.get_user_notifications(
    request.user,
    unread_only=True,
    limit=10
)
```

#### `mark_notification_read(notification_id)`

Mark notification as read.

```python
NotificationService.mark_notification_read(notification_id)
```

#### `mark_all_read(user)`

Mark all as read.

```python
NotificationService.mark_all_read(request.user)
```

#### `get_notification_count(user)`

Get unread count.

```python
unread_count = NotificationService.get_notification_count(request.user)
```

---

### 5. RecommendationService

Generates personalized recommendations for jobs, courses, mentors, and skills.

**Key Methods:**

#### `recommend_jobs(user, limit=10)`

Recommend jobs based on skills.

```python
jobs = RecommendationService.recommend_jobs(request.user, limit=5)
# Returns: [
#   {
#     'job_id': 1,
#     'title': 'Senior Python Developer',
#     'company_name': 'TechCorp',
#     'location': 'San Francisco',
#     'skill_match_percentage': 85,
#     'reason': '85% of your skills match'
#   }
# ]
```

#### `recommend_courses(user, limit=10)`

Recommend courses for skill gaps.

```python
courses = RecommendationService.recommend_courses(request.user, limit=5)
```

#### `recommend_mentors(user, limit=5)`

Recommend mentors.

```python
mentors = RecommendationService.recommend_mentors(request.user, limit=3)
```

#### `recommend_skills(user, limit=5)`

Recommend skills to learn.

```python
skills = RecommendationService.recommend_skills(request.user, limit=5)
```

#### `recommend_connections(user, limit=5)`

Recommend users to connect with.

```python
users = RecommendationService.recommend_connections(request.user, limit=5)
# Returns users with similar skills
```

#### `get_personalized_dashboard(user)`

Get all recommendations at once.

```python
dashboard = RecommendationService.get_personalized_dashboard(request.user)
# Returns: {
#   'recommended_jobs': [...],
#   'recommended_courses': [...],
#   'recommended_mentors': [...],
#   'recommended_skills': [...],
#   'recommended_connections': [...]
# }
```

---

### 6. AnalyticsService

Tracks user activity and generates reports.

**Key Methods:**

#### `get_user_stats(user)`

Get comprehensive user statistics.

```python
stats = AnalyticsService.get_user_stats(request.user)
# Returns: {
#   'profile': {...},
#   'achievements': {...},
#   'skills': {...},
#   'learning': {...},
#   'community': {...},
#   'jobs': {...},
#   'mentoring': {...}
# }
```

#### `get_platform_stats()`

Get platform-wide statistics.

```python
platform_stats = AnalyticsService.get_platform_stats()
# Returns: {
#   'users': {...},
#   'content': {...},
#   'engagement': {...},
#   'jobs': {...}
# }
```

#### `get_activity_heatmap(days=30)`

Get activity heatmap for last N days.

```python
heatmap = AnalyticsService.get_activity_heatmap(days=30)
# Returns: {'2025-01-05': 45, '2025-01-04': 32, ...}
```

#### `get_skill_analytics()`

Get skill analytics.

```python
skill_data = AnalyticsService.get_skill_analytics()
# Returns: {
#   'most_endorsed_skills': [...],
#   'most_common_skills': [...],
#   'expert_count_by_skill': [...]
# }
```

#### `get_course_analytics()`

Get course enrollment analytics.

```python
course_data = AnalyticsService.get_course_analytics()
```

#### `get_job_analytics()`

Get job application analytics.

```python
job_data = AnalyticsService.get_job_analytics()
```

#### `generate_engagement_report(user_id=None)`

Generate complete engagement report.

```python
report = AnalyticsService.generate_engagement_report(user_id=None)
# user_id=None for platform report, or specific user ID
```

---

## Usage in Views

### Example: Resume Upload View

```python
from rest_framework.response import Response
from services import ResumeService, AchievementService, NotificationService

class ResumeViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['post'])
    def upload(self, request):
        try:
            resume = ResumeService.upload_and_analyze_resume(
                user=request.user,
                resume_file=request.FILES['file'],
                file_type=request.data.get('file_type', 'pdf')
            )

            # Check for achievements
            AchievementService.check_and_unlock_achievements(request.user)

            return Response({
                'success': True,
                'resume': ResumeSerializer(resume).data
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)
```

### Example: Dashboard View

```python
from services import RecommendationService, AnalyticsService

class DashboardView(APIView):
    def get(self, request):
        user_stats = AnalyticsService.get_user_stats(request.user)
        recommendations = RecommendationService.get_personalized_dashboard(request.user)

        return Response({
            'stats': user_stats,
            'recommendations': recommendations
        })
```

---

## Integration with Celery Tasks

Services work well with async tasks for heavy operations:

```python
# tasks.py
from celery import shared_task
from services import ResumeService, AnalyticsService

@shared_task
def analyze_resume_async(user_id, resume_id):
    user = User.objects.get(id=user_id)
    resume = Resume.objects.get(id=resume_id)

    # Process resume
    ResumeService._sync_identified_skills(user, resume.extracted_skills)

@shared_task
def cache_platform_analytics():
    AnalyticsService.cache_analytics()
```

---

## Best Practices

1. **Use Services in Views** - Keep views thin by using services
2. **Transaction Management** - Services handle database transactions
3. **Logging** - All services log important operations
4. **Error Handling** - Services raise descriptive exceptions
5. **Caching** - Services use Django cache for performance
6. **Async Operations** - Integrate with Celery for heavy tasks

---

## File Structure

```
services/
├── __init__.py                  # Exports
├── resume_service.py            # Resume processing & ML analysis
├── skill_service.py             # Skill management
├── achievement_service.py        # Gamification
├── notification_service.py       # User notifications
├── recommendation_service.py      # Recommendations
└── analytics_service.py          # Analytics & reporting
```
