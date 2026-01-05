"""
Achievement and gamification tasks.
Checks for and unlocks achievements based on user activity.
"""

import logging
from celery import shared_task
from api.models import User
from services import AchievementService, NotificationService
from tasks.email_tasks import send_achievement_email

logger = logging.getLogger(__name__)


@shared_task
def check_user_achievements(user_id):
    """
    Check and unlock eligible achievements for a user.
    
    Args:
        user_id: User ID
    """
    try:
        user = User.objects.get(id=user_id)
        
        AchievementService.check_and_unlock_achievements(user)
        
        logger.info(f"Achievements checked for user {user_id}")
    
    except User.DoesNotExist:
        logger.warning(f"User {user_id} not found")
    except Exception as exc:
        logger.error(f"Error checking achievements for user {user_id}: {str(exc)}")


@shared_task
def check_all_user_achievements():
    """
    Check and unlock achievements for all users.
    Periodic task that runs hourly.
    """
    try:
        users = User.objects.filter(is_active=True)
        
        for user in users:
            check_user_achievements.delay(user.id)
        
        logger.info(f"Queued achievement checks for {users.count()} users")
    
    except Exception as exc:
        logger.error(f"Error in batch achievement check: {str(exc)}")


@shared_task(bind=True, max_retries=3)
def unlock_achievement_async(self, user_id, achievement_key):
    """
    Unlock an achievement for a user with notifications.
    
    Args:
        user_id: User ID
        achievement_key: Achievement key identifier
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Unlock achievement
        AchievementService.unlock_achievement(user, achievement_key)
        
        # Get achievement details
        from api.models import Achievement
        achievement = Achievement.objects.get(key=achievement_key)
        
        # Send notification
        NotificationService.notify_achievement_unlocked(user, achievement)
        
        # Send email asynchronously
        send_achievement_email.delay(user_id, achievement.name, achievement.points_awarded)
        
        logger.info(f"Achievement {achievement_key} unlocked for user {user_id}")
    
    except Exception as exc:
        logger.error(f"Error unlocking achievement: {str(exc)}")
        raise self.retry(exc=exc, countdown=60, max_retries=3)


@shared_task
def generate_achievement_stats():
    """
    Generate and cache achievement statistics.
    """
    try:
        from services import AnalyticsService
        
        # Get achievement leaderboard
        leaderboard = AchievementService.get_leaderboard(limit=100)
        
        # Cache for 1 hour
        from django.core.cache import cache
        cache.set('achievement_leaderboard', leaderboard, timeout=3600)
        
        logger.info("Achievement statistics generated and cached")
    
    except Exception as exc:
        logger.error(f"Error generating achievement stats: {str(exc)}")


@shared_task
def detect_milestone_achievements():
    """
    Detect and unlock milestone achievements.
    Checks for specific point thresholds.
    """
    try:
        milestones = {
            250: 'legend',
            500: 'legend_plus',  # Could add more levels
        }
        
        users = User.objects.filter(is_active=True)
        
        for user in users:
            for points_threshold, achievement_key in milestones.items():
                if user.points >= points_threshold:
                    from api.models import UserAchievement
                    if not UserAchievement.objects.filter(
                        user=user,
                        achievement__key=achievement_key
                    ).exists():
                        unlock_achievement_async.delay(user.id, achievement_key)
        
        logger.info(f"Checked milestone achievements for {users.count()} users")
    
    except Exception as exc:
        logger.error(f"Error detecting milestone achievements: {str(exc)}")
