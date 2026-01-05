"""
Celery configuration and initialization.
"""

import os
from celery import Celery
from django.conf import settings

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Create Celery app
app = Celery('backend')

# Load configuration from Django settings with namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
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
        'schedule': 86400.0,  # Every day at specific time
    },
}

# Celery settings
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    result_expires=3600,  # Results expire after 1 hour
)

@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery."""
    print(f'Request: {self.request!r}')
