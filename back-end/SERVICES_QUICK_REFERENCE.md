# Services Quick Reference

## All Services

```python
from services import (
    ResumeService,
    SkillService,
    AchievementService,
    NotificationService,
    RecommendationService,
    AnalyticsService
)
```

---

## ResumeService

| Method                        | Purpose                           |
| ----------------------------- | --------------------------------- |
| `upload_and_analyze_resume()` | Upload resume and run ML analysis |
| `get_resume_analysis()`       | Get detailed analysis results     |
| `compare_resumes()`           | Compare two resumes               |
| `delete_resume()`             | Delete a resume                   |

**Example:**

```python
resume = ResumeService.upload_and_analyze_resume(user, file, 'pdf')
print(f"Score: {resume.total_score}, Skills: {resume.extracted_skills}")
```

---

## SkillService

| Method                     | Purpose                         |
| -------------------------- | ------------------------------- |
| `add_skill_to_user()`      | Add skill to user profile       |
| `remove_skill_from_user()` | Remove skill                    |
| `endorse_skill()`          | Endorse another user's skill    |
| `get_skill_gaps()`         | Get recommended skills to learn |
| `get_trending_skills()`    | Get trending skills             |
| `get_skill_demand()`       | Get in-demand skills            |
| `batch_add_skills()`       | Add multiple skills             |

**Example:**

```python
skill = SkillService.add_skill_to_user(user, skill_id=1, proficiency_level='advanced')
gaps = SkillService.get_skill_gaps(user)  # Get top 10 to learn
trending = SkillService.get_trending_skills()  # Top 20 trending
```

---

## AchievementService

| Method                            | Purpose                                  |
| --------------------------------- | ---------------------------------------- |
| `check_and_unlock_achievements()` | Auto-unlock eligible achievements        |
| `unlock_achievement()`            | Manually unlock achievement              |
| `get_user_achievements()`         | Get user's earned achievements           |
| `get_achievement_progress()`      | Get progress towards locked achievements |
| `get_leaderboard()`               | Get achievement leaderboard              |
| `reset_achievement()`             | Remove achievement (admin)               |

**Example:**

```python
AchievementService.check_and_unlock_achievements(user)
achievements = AchievementService.get_user_achievements(user)
leaderboard = AchievementService.get_leaderboard(limit=50)
```

**Achievement Keys:**

- `first_post` (10 pts)
- `first_resume` (15 pts)
- `first_course` (20 pts)
- `course_completion` (50 pts)
- `skill_endorser` (25 pts)
- `mentor` (100 pts)
- `job_seeker` (30 pts)
- `community_leader` (75 pts)
- `skill_master` (60 pts)
- `legend` (250 pts)

---

## NotificationService

| Method                          | Purpose                     |
| ------------------------------- | --------------------------- |
| `create_notification()`         | Create notification         |
| `notify_achievement_unlocked()` | Achievement notification    |
| `notify_job_match()`            | Job match notification      |
| `notify_mentor_request()`       | Mentor request notification |
| `get_user_notifications()`      | Get user's notifications    |
| `mark_notification_read()`      | Mark one as read            |
| `mark_all_read()`               | Mark all as read            |
| `get_notification_count()`      | Get unread count            |

**Example:**

```python
NotificationService.create_notification(user, 'achievement', 'Title', 'Message')
unread = NotificationService.get_notification_count(user)
NotificationService.mark_all_read(user)
```

**Notification Types:**

- `achievement`
- `mention`
- `like`
- `comment`
- `job_match`
- `mentor_request`
- `system`

---

## RecommendationService

| Method                         | Purpose                          |
| ------------------------------ | -------------------------------- |
| `recommend_jobs()`             | Recommend jobs by skill match    |
| `recommend_courses()`          | Recommend courses for skill gaps |
| `recommend_mentors()`          | Recommend mentors                |
| `recommend_skills()`           | Recommend skills to learn        |
| `recommend_connections()`      | Recommend users to connect with  |
| `get_personalized_dashboard()` | Get all recommendations          |

**Example:**

```python
jobs = RecommendationService.recommend_jobs(user, limit=10)
courses = RecommendationService.recommend_courses(user, limit=5)
dashboard = RecommendationService.get_personalized_dashboard(user)
```

---

## AnalyticsService

| Method                         | Purpose                  |
| ------------------------------ | ------------------------ |
| `get_user_stats()`             | Get user's statistics    |
| `get_platform_stats()`         | Get platform-wide stats  |
| `get_activity_heatmap()`       | Get activity chart data  |
| `get_skill_analytics()`        | Get skill statistics     |
| `get_course_analytics()`       | Get course statistics    |
| `get_job_analytics()`          | Get job statistics       |
| `get_mentoring_analytics()`    | Get mentoring statistics |
| `generate_engagement_report()` | Generate complete report |
| `cache_analytics()`            | Cache expensive stats    |

**Example:**

```python
user_stats = AnalyticsService.get_user_stats(user)
platform_stats = AnalyticsService.get_platform_stats()
report = AnalyticsService.generate_engagement_report()
```

---

## Common Patterns

### User Registration Flow

```python
# After user signup
AchievementService.check_and_unlock_achievements(new_user)
```

### Resume Upload Flow

```python
resume = ResumeService.upload_and_analyze_resume(user, file, 'pdf')
AchievementService.check_and_unlock_achievements(user)
NotificationService.create_notification(user, 'system', 'Resume Analyzed', 'Your resume has been analyzed')
```

### Job Recommendation Flow

```python
jobs = RecommendationService.recommend_jobs(user)
for job in jobs:
    NotificationService.notify_job_match(user, job)
```

### Dashboard Data

```python
dashboard = {
    'user_stats': AnalyticsService.get_user_stats(user),
    'recommendations': RecommendationService.get_personalized_dashboard(user),
    'achievements': AchievementService.get_user_achievements(user),
}
```

---

## Integration with Views

### In ViewSets

```python
from services import ResumeService, AchievementService

class ResumeViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        resume = serializer.save(user=self.request.user)
        AchievementService.check_and_unlock_achievements(self.request.user)
```

### In APIView

```python
from services import RecommendationService, AnalyticsService
from rest_framework.views import APIView

class DashboardAPIView(APIView):
    def get(self, request):
        return Response({
            'recommendations': RecommendationService.get_personalized_dashboard(request.user),
            'stats': AnalyticsService.get_user_stats(request.user),
        })
```

---

## Celery Integration

```python
# tasks.py
from celery import shared_task
from services import AnalyticsService, RecommendationService

@shared_task
def cache_platform_analytics():
    AnalyticsService.cache_analytics()

@shared_task
def generate_daily_recommendations(user_id):
    user = User.objects.get(id=user_id)
    dashboard = RecommendationService.get_personalized_dashboard(user)
    # Store or email recommendations
```

---

## Caching

Services use Django cache:

```python
from django.core.cache import cache

# Analytics caching
cache.set('platform_stats', stats_dict, timeout=3600)
stats = cache.get('platform_stats')

# User activity tracking
cache.set(f'user_actions:{user_id}', actions_list, timeout=86400)
```

---

## Error Handling

```python
try:
    resume = ResumeService.upload_and_analyze_resume(user, file, 'pdf')
except Exception as e:
    logger.error(f"Resume analysis failed: {str(e)}")
    NotificationService.create_notification(user, 'system', 'Error', f'Resume analysis failed: {str(e)}')
```

---

## Testing

```python
from django.test import TestCase
from services import SkillService, AchievementService

class SkillServiceTestCase(TestCase):
    def test_add_skill_to_user(self):
        user = User.objects.create_user(username='test')
        skill = Skill.objects.create(name='Python')

        user_skill = SkillService.add_skill_to_user(user, skill.id)
        self.assertEqual(user_skill.skill, skill)

    def test_skill_gaps(self):
        user = User.objects.create_user(username='test')
        gaps = SkillService.get_skill_gaps(user)
        self.assertIsInstance(gaps, list)
```

---

## Performance Tips

1. **Cache expensive operations** - Use `cache_analytics()`
2. **Batch operations** - Use `batch_add_skills()` for multiple skills
3. **Limit results** - Use `limit` parameter on recommendations
4. **Async tasks** - Use Celery for heavy processing
5. **Database optimization** - Services use select_related/prefetch_related
