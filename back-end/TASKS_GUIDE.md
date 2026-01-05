# Celery Tasks Documentation

## Overview

The tasks module contains asynchronous job definitions using Celery. Tasks handle email notifications, resume processing, recommendations, achievements, notifications, and analytics.

---

## Configuration

### Celery Setup

File: `tasks/celery.py`

```python
from celery import Celery

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### Django Settings

Add to `settings.py`:

```python
# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
```

### Frontend URL Configuration

```python
# In settings.py
FRONTEND_URL = 'http://localhost:3000'
```

---

## Email Tasks

File: `tasks/email_tasks.py`

### Send Welcome Email

```python
from tasks.email_tasks import send_welcome_email

# Send welcome email to new user
send_welcome_email.delay(user_id)
```

**Template:** `emails/welcome.html`

### Send Achievement Email

```python
from tasks.email_tasks import send_achievement_email

send_achievement_email.delay(
    user_id=1,
    achievement_name='First Post',
    points=10
)
```

**Template:** `emails/achievement.html`

### Send Job Match Email

```python
from tasks.email_tasks import send_job_match_email

send_job_match_email.delay(user_id, job_id)
```

**Template:** `emails/job_match.html`

### Send Mentor Request Email

```python
from tasks.email_tasks import send_mentor_request_email

send_mentor_request_email.delay(mentor_id, session_id)
```

**Template:** `emails/mentor_request.html`

### Send Course Enrollment Email

```python
from tasks.email_tasks import send_course_enrollment_email

send_course_enrollment_email.delay(user_id, course_id)
```

**Template:** `emails/course_enrollment.html`

### Send Daily Digest

```python
from tasks.email_tasks import send_daily_digest

send_daily_digest.delay()  # Called automatically by Celery Beat
```

Sends personalized digest emails to active users with:

- New recommendations
- Achievement progress
- Community highlights

### Send Weekly Report

```python
from tasks.email_tasks import send_weekly_report

send_weekly_report.delay()
```

### Send Password Reset Email

```python
from tasks.email_tasks import send_password_reset_email

send_password_reset_email.delay(user_id, reset_token)
```

---

## Resume Tasks

File: `tasks/resume_tasks.py`

### Analyze Resume Async

```python
from tasks.resume_tasks import analyze_resume_async

analyze_resume_async.delay(resume_id)
```

**What it does:**

1. Extracts text from resume file
2. Performs ML analysis
3. Syncs identified skills with user profile
4. Checks for achievement unlock
5. Sends notification to user

### Extract Resume Text

```python
from tasks.resume_tasks import extract_resume_text_async

extract_resume_text_async.delay(resume_id)
```

### Batch Analyze Resumes

```python
from tasks.resume_tasks import batch_analyze_resumes

batch_analyze_resumes.delay()
```

Analyzes all pending resumes without extracted text.

### Cleanup Old Resumes

```python
from tasks.resume_tasks import cleanup_old_resumes

cleanup_old_resumes.delay(days=90)
```

Deletes soft-deleted resumes older than N days.

---

## Recommendation Tasks

File: `tasks/recommendation_tasks.py`

### Generate Daily Recommendations

```python
from tasks.recommendation_tasks import generate_daily_recommendations

generate_daily_recommendations.delay()  # Runs automatically daily
```

Generates and caches recommendations for all active users.

### Recommend Jobs Async

```python
from tasks.recommendation_tasks import recommend_jobs_async

recommend_jobs_async.delay(user_id, limit=10)
```

Generates and caches job recommendations.

### Recommend Courses Async

```python
from tasks.recommendation_tasks import recommend_courses_async

recommend_courses_async.delay(user_id, limit=10)
```

### Recommend Mentors Async

```python
from tasks.recommendation_tasks import recommend_mentors_async

recommend_mentors_async.delay(user_id, limit=5)
```

### Recommend Skills Async

```python
from tasks.recommendation_tasks import recommend_skills_async

recommend_skills_async.delay(user_id, limit=5)
```

### Recommend Connections Async

```python
from tasks.recommendation_tasks import recommend_connections_async

recommend_connections_async.delay(user_id, limit=5)
```

### Batch Recommend Jobs

```python
from tasks.recommendation_tasks import batch_recommend_jobs

batch_recommend_jobs.delay()
```

Generates job recommendations for all users.

---

## Achievement Tasks

File: `tasks/achievement_tasks.py`

### Check User Achievements

```python
from tasks.achievement_tasks import check_user_achievements

check_user_achievements.delay(user_id)
```

Checks and unlocks eligible achievements for a user.

### Check All User Achievements

```python
from tasks.achievement_tasks import check_all_user_achievements

check_all_user_achievements.delay()  # Runs automatically hourly
```

Checks achievements for all active users.

### Unlock Achievement Async

```python
from tasks.achievement_tasks import unlock_achievement_async

unlock_achievement_async.delay(user_id, 'first_post')
```

Unlocks achievement with notifications and email.

### Generate Achievement Stats

```python
from tasks.achievement_tasks import generate_achievement_stats

generate_achievement_stats.delay()
```

Generates and caches achievement leaderboard.

### Detect Milestone Achievements

```python
from tasks.achievement_tasks import detect_milestone_achievements

detect_milestone_achievements.delay()
```

Detects and unlocks point milestone achievements.

---

## Notification Tasks

File: `tasks/notification_tasks.py`

### Send Notification Async

```python
from tasks.notification_tasks import send_notification_async

send_notification_async.delay(
    user_id=1,
    notification_type='achievement',
    title='Achievement Unlocked!',
    message='You earned the "First Post" achievement',
    related_user_id=None
)
```

### Cleanup Old Notifications

```python
from tasks.notification_tasks import cleanup_old_notifications

cleanup_old_notifications.delay(days=30)  # Runs automatically daily
```

Deletes read notifications older than N days.

### Send Mention Notifications

```python
from tasks.notification_tasks import send_mention_notifications

send_mention_notifications.delay(
    user_ids=[1, 2, 3],
    mention_type='post',
    content_id=5
)
```

### Send Like Notifications

```python
from tasks.notification_tasks import send_like_notifications

send_like_notifications.delay(
    user_id=1,  # Content owner
    liker_id=2,  # User who liked
    content_type='post'
)
```

### Send Comment Notifications

```python
from tasks.notification_tasks import send_comment_notifications

send_comment_notifications.delay(
    user_id=1,
    commenter_id=2,
    content_type='post'
)
```

### Mark Notifications Read Batch

```python
from tasks.notification_tasks import mark_notifications_read_batch

mark_notifications_read_batch.delay(user_id)
```

### Send Batch Notifications

```python
from tasks.notification_tasks import send_batch_notifications

send_batch_notifications.delay([
    {
        'user_id': 1,
        'notification_type': 'achievement',
        'title': '...',
        'message': '...'
    }
])
```

---

## Analytics Tasks

File: `tasks/analytics_tasks.py`

### Cache Platform Analytics

```python
from tasks.analytics_tasks import cache_platform_analytics

cache_platform_analytics.delay()  # Runs automatically hourly
```

Caches expensive analytics computations:

- Platform stats
- Skill analytics
- Course analytics
- Job analytics
- Mentoring analytics

### Cache User Analytics

```python
from tasks.analytics_tasks import cache_user_analytics

cache_user_analytics.delay(user_id)
```

### Generate Activity Heatmap

```python
from tasks.analytics_tasks import generate_activity_heatmap

generate_activity_heatmap.delay(days=30)
```

### Generate User Growth Report

```python
from tasks.analytics_tasks import generate_user_growth_report

generate_user_growth_report.delay()
```

### Batch Cache User Analytics

```python
from tasks.analytics_tasks import batch_cache_user_analytics

batch_cache_user_analytics.delay()
```

Caches analytics for all active users.

### Generate Daily Report

```python
from tasks.analytics_tasks import generate_daily_report

generate_daily_report.delay()
```

Generates comprehensive daily platform report.

### Export Analytics Snapshot

```python
from tasks.analytics_tasks import export_analytics_snapshot

export_analytics_snapshot.delay()
```

Exports analytics data for archiving.

---

## Celery Beat Schedule

Automatic scheduled tasks in `settings.py`:

```python
CELERY_BEAT_SCHEDULE = {
    'cache-platform-analytics': {
        'task': 'tasks.analytics_tasks.cache_platform_analytics',
        'schedule': 3600.0,  # Every hour
    },
    'check-user-achievements': {
        'task': 'tasks.achievement_tasks.check_all_user_achievements',
        'schedule': 3600.0,  # Every hour
    },
    'generate-daily-recommendations': {
        'task': 'tasks.recommendation_tasks.generate_daily_recommendations',
        'schedule': 86400.0,  # Every day
    },
    'cleanup-old-notifications': {
        'task': 'tasks.notification_tasks.cleanup_old_notifications',
        'schedule': 86400.0,  # Every day
    },
    'send-daily-digest': {
        'task': 'tasks.email_tasks.send_daily_digest',
        'schedule': 86400.0,  # Every day
    },
}
```

---

## Running Celery

### Start Worker

```bash
celery -A tasks worker -l info
```

### Start Beat Scheduler

```bash
celery -A tasks beat -l info
```

### Run Both (Development)

```bash
celery -A tasks worker -B -l info
```

### Monitor Tasks

```bash
# Install flower
pip install flower

# Run Flower (web UI on http://localhost:5555)
celery -A tasks flower
```

---

## Usage in Views

### Example: Resume Upload

```python
from tasks.resume_tasks import analyze_resume_async
from rest_framework.response import Response
from rest_framework.decorators import action

class ResumeViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['post'])
    def upload(self, request):
        serializer = ResumeSerializer(data=request.data)

        if serializer.is_valid():
            resume = serializer.save(user=request.user)

            # Analyze asynchronously
            analyze_resume_async.delay(resume.id)

            return Response({
                'success': True,
                'resume_id': resume.id,
                'message': 'Resume is being analyzed'
            })

        return Response(serializer.errors, status=400)
```

### Example: Job Application

```python
from tasks.notification_tasks import send_notification_async
from tasks.recommendation_tasks import recommend_jobs_async

class JobApplicationViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        application = serializer.save(user=self.request.user)

        # Queue recommendation update
        recommend_jobs_async.delay(self.request.user.id, limit=10)
```

---

## Error Handling

Tasks use retry mechanism with exponential backoff:

```python
@shared_task(bind=True, max_retries=3)
def my_task(self, user_id):
    try:
        # Do work
        pass
    except Exception as exc:
        # Retry after 60 seconds, up to 3 times
        raise self.retry(exc=exc, countdown=60, max_retries=3)
```

---

## Best Practices

1. **Use delay() for fire-and-forget tasks**

   ```python
   send_welcome_email.delay(user_id)
   ```

2. **Chain tasks for dependencies**

   ```python
   from celery import chain

   chain(
       analyze_resume_async.s(resume_id),
       check_user_achievements.s(user_id)
   ).apply_async()
   ```

3. **Use groups for parallel tasks**

   ```python
   from celery import group

   job = group(
       recommend_jobs_async.s(user_id),
       recommend_courses_async.s(user_id)
   )
   job.apply_async()
   ```

4. **Monitor task status**

   ```python
   from celery.result import AsyncResult

   task_id = 'task-uuid'
   result = AsyncResult(task_id)
   print(result.status)  # PENDING, STARTED, SUCCESS, FAILURE
   ```

5. **Set task timeouts**
   ```python
   @shared_task(time_limit=300)  # 5 minutes
   def long_running_task():
       pass
   ```

---

## Troubleshooting

### Tasks Not Running

1. Check Celery worker is running
2. Verify Redis is accessible
3. Check logs for errors: `celery -A tasks worker -l debug`

### Email Not Sending

1. Verify email settings in `settings.py`
2. Check SMTP credentials
3. Review email task logs

### High Memory Usage

1. Reduce result backend timeout
2. Use task rate limiting
3. Monitor with Flower

---

## Performance Optimization

1. **Use task routing** - Send tasks to specific workers
2. **Set task priority** - Important tasks first
3. **Cache results** - Avoid re-computing
4. **Batch operations** - Group similar tasks
5. **Monitor workers** - Use Flower dashboard
