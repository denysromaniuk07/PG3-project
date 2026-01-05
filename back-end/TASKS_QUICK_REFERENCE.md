# Tasks Quick Reference

## Email Tasks

```python
from tasks.email_tasks import (
    send_welcome_email,
    send_achievement_email,
    send_job_match_email,
    send_mentor_request_email,
    send_course_enrollment_email,
    send_daily_digest,
    send_weekly_report,
    send_password_reset_email,
)
```

| Task                             | Usage                        |
| -------------------------------- | ---------------------------- |
| `send_welcome_email()`           | New user signup              |
| `send_achievement_email()`       | Achievement unlock           |
| `send_job_match_email()`         | Job recommendation           |
| `send_mentor_request_email()`    | Mentor request received      |
| `send_course_enrollment_email()` | Course enrollment            |
| `send_daily_digest()`            | Daily recommendations (auto) |
| `send_weekly_report()`           | Weekly summary               |
| `send_password_reset_email()`    | Password reset               |

**Example:**

```python
send_welcome_email.delay(user_id)
send_achievement_email.delay(user_id, 'Achievement Name', 10)
```

---

## Resume Tasks

```python
from tasks.resume_tasks import (
    analyze_resume_async,
    extract_resume_text_async,
    batch_analyze_resumes,
    cleanup_old_resumes,
)
```

| Task                          | Purpose            |
| ----------------------------- | ------------------ |
| `analyze_resume_async()`      | ML analysis        |
| `extract_resume_text_async()` | Text extraction    |
| `batch_analyze_resumes()`     | Batch processing   |
| `cleanup_old_resumes()`       | Delete old resumes |

**Example:**

```python
analyze_resume_async.delay(resume_id)
batch_analyze_resumes.delay()
cleanup_old_resumes.delay(days=90)
```

---

## Recommendation Tasks

```python
from tasks.recommendation_tasks import (
    generate_daily_recommendations,
    recommend_jobs_async,
    recommend_courses_async,
    recommend_mentors_async,
    recommend_skills_async,
    recommend_connections_async,
    batch_recommend_jobs,
)
```

| Task                               | Purpose                |
| ---------------------------------- | ---------------------- |
| `generate_daily_recommendations()` | All recs (auto)        |
| `recommend_jobs_async()`           | Job recommendations    |
| `recommend_courses_async()`        | Course recommendations |
| `recommend_mentors_async()`        | Mentor recommendations |
| `recommend_skills_async()`         | Skill recommendations  |
| `recommend_connections_async()`    | User recommendations   |
| `batch_recommend_jobs()`           | Batch job recs         |

**Example:**

```python
recommend_jobs_async.delay(user_id, limit=10)
generate_daily_recommendations.delay()
```

---

## Achievement Tasks

```python
from tasks.achievement_tasks import (
    check_user_achievements,
    check_all_user_achievements,
    unlock_achievement_async,
    generate_achievement_stats,
    detect_milestone_achievements,
)
```

| Task                              | Purpose           |
| --------------------------------- | ----------------- |
| `check_user_achievements()`       | Check for unlocks |
| `check_all_user_achievements()`   | All users (auto)  |
| `unlock_achievement_async()`      | Unlock + notify   |
| `generate_achievement_stats()`    | Leaderboard       |
| `detect_milestone_achievements()` | Points milestones |

**Example:**

```python
check_user_achievements.delay(user_id)
unlock_achievement_async.delay(user_id, 'first_post')
```

---

## Notification Tasks

```python
from tasks.notification_tasks import (
    send_notification_async,
    cleanup_old_notifications,
    send_mention_notifications,
    send_like_notifications,
    send_comment_notifications,
    mark_notifications_read_batch,
    send_batch_notifications,
)
```

| Task                              | Purpose              |
| --------------------------------- | -------------------- |
| `send_notification_async()`       | Single notification  |
| `cleanup_old_notifications()`     | Delete old (auto)    |
| `send_mention_notifications()`    | Mention bulk         |
| `send_like_notifications()`       | Like notification    |
| `send_comment_notifications()`    | Comment notification |
| `mark_notifications_read_batch()` | Mark all read        |
| `send_batch_notifications()`      | Batch send           |

**Example:**

```python
send_notification_async.delay(user_id, 'achievement', 'Title', 'Message')
send_mention_notifications.delay([1, 2, 3], 'post', 5)
```

---

## Analytics Tasks

```python
from tasks.analytics_tasks import (
    cache_platform_analytics,
    cache_user_analytics,
    generate_activity_heatmap,
    generate_user_growth_report,
    batch_cache_user_analytics,
    generate_daily_report,
    export_analytics_snapshot,
)
```

| Task                            | Purpose               |
| ------------------------------- | --------------------- |
| `cache_platform_analytics()`    | Platform stats (auto) |
| `cache_user_analytics()`        | User stats            |
| `generate_activity_heatmap()`   | Activity chart        |
| `generate_user_growth_report()` | User growth           |
| `batch_cache_user_analytics()`  | All users             |
| `generate_daily_report()`       | Daily report          |
| `export_analytics_snapshot()`   | Archive snapshot      |

**Example:**

```python
cache_platform_analytics.delay()
cache_user_analytics.delay(user_id)
generate_daily_report.delay()
```

---

## Common Patterns

### User Registration

```python
from tasks.email_tasks import send_welcome_email
from tasks.achievement_tasks import check_user_achievements

# After user creation
send_welcome_email.delay(new_user.id)
check_user_achievements.delay(new_user.id)
```

### Resume Upload

```python
from tasks.resume_tasks import analyze_resume_async

resume = Resume.objects.create(...)
analyze_resume_async.delay(resume.id)
```

### Job Application

```python
from tasks.recommendation_tasks import recommend_jobs_async

JobApplication.objects.create(...)
recommend_jobs_async.delay(user_id)
```

### Achievement Unlock

```python
from tasks.achievement_tasks import unlock_achievement_async

unlock_achievement_async.delay(user_id, 'achievement_key')
```

### Post Like/Comment

```python
from tasks.notification_tasks import send_like_notifications

send_like_notifications.delay(post_owner_id, liker_id, 'post')
```

---

## Task States

```
PENDING     - Task is waiting to execute
STARTED     - Task has started executing
SUCCESS     - Task completed successfully
FAILURE     - Task failed
RETRY       - Task is being retried
REVOKED     - Task was revoked
```

Check task status:

```python
from celery.result import AsyncResult

result = AsyncResult(task_id)
print(result.status)
print(result.result)  # Result if SUCCESS
```

---

## Scheduling & Automation

### Celery Beat (Periodic Tasks)

Auto-runs hourly:

- `cache_platform_analytics` - Platform analytics
- `check_all_user_achievements` - Achievement checks

Auto-runs daily:

- `generate_daily_recommendations` - User recommendations
- `cleanup_old_notifications` - Delete old notifications
- `send_daily_digest` - Daily emails

Start Beat scheduler:

```bash
celery -A tasks beat -l info
```

---

## Running Celery

### Start Worker

```bash
celery -A tasks worker -l info
```

### Start Worker + Beat (Dev)

```bash
celery -A tasks worker -B -l info
```

### Monitor with Flower

```bash
pip install flower
celery -A tasks flower
# Visit http://localhost:5555
```

### Check Worker Status

```bash
celery -A tasks inspect active
celery -A tasks inspect registered
celery -A tasks inspect stats
```

---

## Configuration

### Redis Setup

```bash
# Start Redis
redis-server

# Check connection
redis-cli ping
```

### Django Settings

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
```

---

## Error Handling

Tasks retry automatically:

```python
@shared_task(bind=True, max_retries=3)
def my_task(self):
    try:
        # Do work
        pass
    except Exception as exc:
        # Retry after 60 seconds
        raise self.retry(exc=exc, countdown=60)
```

---

## Performance Tips

1. **Use groups for parallel tasks**

   ```python
   from celery import group
   group(task1.s(), task2.s()).apply_async()
   ```

2. **Chain dependent tasks**

   ```python
   from celery import chain
   chain(task1.s(), task2.s()).apply_async()
   ```

3. **Set task timeouts**

   ```python
   @shared_task(time_limit=300)
   def slow_task():
       pass
   ```

4. **Monitor with Flower** - Visual task monitoring

5. **Batch operations** - Combine small tasks

---

## Debugging

### View Task Logs

```bash
celery -A tasks inspect query_task task_id
```

### Test Task Locally

```python
from tasks.email_tasks import send_welcome_email

# Run synchronously
send_welcome_email(user_id)  # Not .delay()
```

### Check Queue

```bash
redis-cli
LRANGE celery 0 -1  # View queued tasks
```
