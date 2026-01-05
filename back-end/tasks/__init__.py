"""
Celery tasks for asynchronous job processing.

This package contains Celery tasks for:
- Email notifications and digests
- Resume analysis and text extraction
- Recommendation generation
- Achievement checking and unlocking
- Notification delivery
- Analytics and reporting
"""

# Import all tasks so Celery can discover them
from . import email_tasks
from . import resume_tasks
from . import recommendation_tasks
from . import achievement_tasks
from . import notification_tasks
from . import analytics_tasks

__all__ = [
    'email_tasks',
    'resume_tasks',
    'recommendation_tasks',
    'achievement_tasks',
    'notification_tasks',
    'analytics_tasks',
]
