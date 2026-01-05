"""
Achievement and gamification service.
Handles achievement unlocking, progress tracking, and reward distribution.
"""

import logging
from django.utils import timezone
from django.db.models import Count
from api.models import Achievement, UserAchievement, User
from datetime import timedelta

logger = logging.getLogger(__name__)


class AchievementService:
    """Service for managing achievements and gamification."""

    # Achievement definitions and unlock conditions
    ACHIEVEMENT_TRIGGERS = {
        'first_post': {
            'name': 'First Post',
            'description': 'Create your first community post',
            'points': 10,
            'rarity': 'common',
            'trigger': 'community_post_count',
            'condition': lambda count: count == 1
        },
        'first_resume': {
            'name': 'Resume Master',
            'description': 'Upload your first resume',
            'points': 15,
            'rarity': 'common',
            'trigger': 'resume_count',
            'condition': lambda count: count == 1
        },
        'first_course': {
            'name': 'Learner',
            'description': 'Enroll in your first course',
            'points': 20,
            'rarity': 'common',
            'trigger': 'course_count',
            'condition': lambda count: count == 1
        },
        'course_completion': {
            'name': 'Course Completer',
            'description': 'Complete a full course',
            'points': 50,
            'rarity': 'rare',
            'trigger': 'completed_course_count',
            'condition': lambda count: count >= 1
        },
        'skill_endorser': {
            'name': 'Skill Endorser',
            'description': 'Endorse 5 different skills',
            'points': 25,
            'rarity': 'rare',
            'trigger': 'endorsements',
            'condition': lambda count: count >= 5
        },
        'mentor': {
            'name': 'Mentor',
            'description': 'Complete 5 mentoring sessions',
            'points': 100,
            'rarity': 'epic',
            'trigger': 'mentor_sessions',
            'condition': lambda count: count >= 5
        },
        'job_seeker': {
            'name': 'Job Seeker',
            'description': 'Apply for 10 jobs',
            'points': 30,
            'rarity': 'rare',
            'trigger': 'job_applications',
            'condition': lambda count: count >= 10
        },
        'community_leader': {
            'name': 'Community Leader',
            'description': 'Reach 100 post likes',
            'points': 75,
            'rarity': 'epic',
            'trigger': 'post_likes',
            'condition': lambda count: count >= 100
        },
        'skill_master': {
            'name': 'Skill Master',
            'description': 'Learn 10 different skills',
            'points': 60,
            'rarity': 'epic',
            'trigger': 'skills_count',
            'condition': lambda count: count >= 10
        },
        'legend': {
            'name': 'Legend',
            'description': 'Reach 1000 platform points',
            'points': 250,
            'rarity': 'legendary',
            'trigger': 'user_points',
            'condition': lambda points: points >= 1000
        }
    }

    @staticmethod
    def check_and_unlock_achievements(user):
        """
        Check user's activity and unlock any new achievements.
        
        Args:
            user: User object
        """
        for achievement_key, achievement_def in AchievementService.ACHIEVEMENT_TRIGGERS.items():
            # Check if user already has this achievement
            if UserAchievement.objects.filter(user=user, achievement__key=achievement_key).exists():
                continue
            
            # Get the metric value
            metric_value = AchievementService._get_metric_value(user, achievement_def['trigger'])
            
            # Check if condition is met
            if achievement_def['condition'](metric_value):
                AchievementService.unlock_achievement(user, achievement_key)

    @staticmethod
    def unlock_achievement(user, achievement_key):
        """
        Unlock an achievement for a user.
        
        Args:
            user: User object
            achievement_key: Achievement key identifier
        """
        achievement_def = AchievementService.ACHIEVEMENT_TRIGGERS.get(achievement_key)
        if not achievement_def:
            logger.warning(f"Unknown achievement key: {achievement_key}")
            return
        
        # Get or create achievement
        achievement, created = Achievement.objects.get_or_create(
            key=achievement_key,
            defaults={
                'name': achievement_def['name'],
                'description': achievement_def['description'],
                'points_awarded': achievement_def['points'],
                'rarity': achievement_def['rarity'],
                'icon': f'achievements/{achievement_key}.svg'
            }
        )
        
        # Create user achievement
        user_achievement, created = UserAchievement.objects.get_or_create(
            user=user,
            achievement=achievement,
            defaults={'earned_at': timezone.now()}
        )
        
        if created:
            # Award points to user
            user.points += achievement.points_awarded
            user.save()
            
            logger.info(f"Achievement {achievement_key} unlocked for user {user.id}, +{achievement.points_awarded} points")

    @staticmethod
    def _get_metric_value(user, metric_type):
        """
        Get metric value for achievement checking.
        
        Args:
            user: User object
            metric_type: Type of metric to retrieve
        
        Returns:
            Metric value
        """
        from api.models import (
            CommunityPost, Resume, UserCourseProgress,
            UserSkill, MentorSession, JobApplication
        )
        
        metrics = {
            'community_post_count': lambda: CommunityPost.objects.filter(author=user).count(),
            'resume_count': lambda: Resume.objects.filter(user=user).count(),
            'course_count': lambda: UserCourseProgress.objects.filter(user=user).count(),
            'completed_course_count': lambda: UserCourseProgress.objects.filter(user=user, status='completed').count(),
            'endorsements': lambda: UserSkill.objects.filter(user=user).aggregate(
                total=Count('endorsements_count')
            )['total'] or 0,
            'mentor_sessions': lambda: MentorSession.objects.filter(mentor=user, status='completed').count(),
            'job_applications': lambda: JobApplication.objects.filter(user=user).count(),
            'post_likes': lambda: CommunityPost.objects.filter(author=user).aggregate(
                total=Count('likes_count')
            )['total'] or 0,
            'skills_count': lambda: UserSkill.objects.filter(user=user).count(),
            'user_points': lambda: user.points,
        }
        
        return metrics.get(metric_type, lambda: 0)()

    @staticmethod
    def get_user_achievements(user):
        """
        Get all achievements earned by a user.
        
        Args:
            user: User object
        
        Returns:
            List of earned achievements
        """
        return UserAchievement.objects.filter(user=user).select_related('achievement').order_by('-earned_at')

    @staticmethod
    def get_achievement_progress(user):
        """
        Get user's progress towards locked achievements.
        
        Args:
            user: User object
        
        Returns:
            List of achievements with progress
        """
        earned_keys = set(
            UserAchievement.objects.filter(user=user).values_list('achievement__key', flat=True)
        )
        
        progress = []
        for achievement_key, achievement_def in AchievementService.ACHIEVEMENT_TRIGGERS.items():
            if achievement_key in earned_keys:
                continue
            
            metric_value = AchievementService._get_metric_value(user, achievement_def['trigger'])
            
            # Estimate progress (this is simplified)
            progress.append({
                'achievement_key': achievement_key,
                'name': achievement_def['name'],
                'description': achievement_def['description'],
                'points': achievement_def['points'],
                'rarity': achievement_def['rarity'],
                'current_progress': metric_value,
                'estimated_percentage': min(100, int((metric_value / 10) * 100))  # Simplified
            })
        
        return sorted(progress, key=lambda x: x['estimated_percentage'], reverse=True)

    @staticmethod
    def get_leaderboard(limit=100):
        """
        Get achievement leaderboard based on points.
        
        Args:
            limit: Number of users to return
        
        Returns:
            List of top users with achievement stats
        """
        leaderboard = User.objects.all().order_by('-points')[:limit]
        
        return [{
            'user_id': user.id,
            'username': user.username,
            'points': user.points,
            'achievement_count': UserAchievement.objects.filter(user=user).count(),
            'avatar': user.profile_picture.url if user.profile_picture else None,
        } for user in leaderboard]

    @staticmethod
    def reset_achievement(user, achievement_key):
        """
        Reset (remove) an achievement from a user (admin only).
        
        Args:
            user: User object
            achievement_key: Achievement key
        """
        user_achievement = UserAchievement.objects.filter(
            user=user,
            achievement__key=achievement_key
        ).first()
        
        if user_achievement:
            achievement = user_achievement.achievement
            user.points -= achievement.points_awarded
            user.save()
            user_achievement.delete()
            logger.info(f"Achievement {achievement_key} reset for user {user.id}")
