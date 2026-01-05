"""
Analytics tasks.
Generates and caches analytics data periodically.
"""

import logging
from celery import shared_task
from django.core.cache import cache
from services import AnalyticsService

logger = logging.getLogger(__name__)


@shared_task
def cache_platform_analytics():
    """
    Cache expensive analytics computations hourly.
    """
    try:
        # Cache platform stats
        platform_stats = AnalyticsService.get_platform_stats()
        cache.set('platform_stats', platform_stats, timeout=3600)
        
        # Cache skill analytics
        skill_analytics = AnalyticsService.get_skill_analytics()
        cache.set('skill_analytics', skill_analytics, timeout=3600)
        
        # Cache course analytics
        course_analytics = AnalyticsService.get_course_analytics()
        cache.set('course_analytics', course_analytics, timeout=3600)
        
        # Cache job analytics
        job_analytics = AnalyticsService.get_job_analytics()
        cache.set('job_analytics', job_analytics, timeout=3600)
        
        # Cache mentoring analytics
        mentoring_analytics = AnalyticsService.get_mentoring_analytics()
        cache.set('mentoring_analytics', mentoring_analytics, timeout=3600)
        
        logger.info("Platform analytics cached successfully")
    
    except Exception as exc:
        logger.error(f"Error caching platform analytics: {str(exc)}")


@shared_task
def cache_user_analytics(user_id):
    """
    Cache user-specific analytics.
    
    Args:
        user_id: User ID
    """
    try:
        from api.models import User
        
        user = User.objects.get(id=user_id)
        stats = AnalyticsService.get_user_stats(user)
        
        cache.set(f'user_stats:{user_id}', stats, timeout=3600)
        
        logger.info(f"User analytics cached for user {user_id}")
    
    except Exception as exc:
        logger.error(f"Error caching user analytics: {str(exc)}")


@shared_task
def generate_activity_heatmap(days=30):
    """
    Generate and cache activity heatmap.
    
    Args:
        days: Number of days to include
    """
    try:
        heatmap = AnalyticsService.get_activity_heatmap(days=days)
        cache.set('activity_heatmap', heatmap, timeout=3600)
        
        logger.info(f"Activity heatmap generated for {days} days")
    
    except Exception as exc:
        logger.error(f"Error generating activity heatmap: {str(exc)}")


@shared_task
def generate_user_growth_report():
    """
    Generate and cache user growth data.
    """
    try:
        growth = AnalyticsService.get_user_growth()
        cache.set('user_growth', growth, timeout=86400)  # Cache for 24 hours
        
        logger.info("User growth report generated and cached")
    
    except Exception as exc:
        logger.error(f"Error generating growth report: {str(exc)}")


@shared_task
def batch_cache_user_analytics():
    """
    Cache analytics for all active users.
    """
    try:
        from api.models import User
        
        users = User.objects.filter(is_active=True)
        
        for user in users:
            cache_user_analytics.delay(user.id)
        
        logger.info(f"Queued analytics caching for {users.count()} users")
    
    except Exception as exc:
        logger.error(f"Error in batch user analytics: {str(exc)}")


@shared_task
def generate_daily_report():
    """
    Generate daily platform report and cache it.
    """
    try:
        from django.utils import timezone
        
        report = {
            'generated_at': timezone.now().isoformat(),
            'platform_stats': AnalyticsService.get_platform_stats(),
            'skill_analytics': AnalyticsService.get_skill_analytics(),
            'course_analytics': AnalyticsService.get_course_analytics(),
            'job_analytics': AnalyticsService.get_job_analytics(),
        }
        
        # Cache report
        cache.set('daily_report', report, timeout=86400)  # 24 hours
        
        logger.info("Daily report generated and cached")
    
    except Exception as exc:
        logger.error(f"Error generating daily report: {str(exc)}")


@shared_task
def export_analytics_snapshot():
    """
    Export analytics snapshot for archiving or reporting.
    """
    try:
        from django.utils import timezone
        import json
        
        snapshot = {
            'timestamp': timezone.now().isoformat(),
            'platform_stats': AnalyticsService.get_platform_stats(),
            'skill_analytics': AnalyticsService.get_skill_analytics(),
            'user_growth': AnalyticsService.get_user_growth(),
        }
        
        # Could save to database, file storage, or external service
        cache.set(
            f'analytics_snapshot:{timezone.now().strftime("%Y-%m-%d")}',
            snapshot,
            timeout=2592000  # 30 days
        )
        
        logger.info("Analytics snapshot exported")
    
    except Exception as exc:
        logger.error(f"Error exporting analytics snapshot: {str(exc)}")
