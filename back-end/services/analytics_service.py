"""
Analytics service.
Tracks user activity, platform metrics, and generates reports.
"""

import logging
from django.utils import timezone
from django.db.models import Count, Q, F, Sum, Avg
from api.models import (
    User, CommunityPost, Resume, UserCourseProgress,
    UserSkill, MentorSession, JobApplication, UserAchievement
)
from datetime import timedelta, datetime
from django.core.cache import cache

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for tracking analytics and generating reports."""

    @staticmethod
    def get_user_stats(user):
        """
        Get comprehensive statistics for a user.
        
        Args:
            user: User object
        
        Returns:
            Dictionary of user statistics
        """
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        
        return {
            'profile': {
                'points': user.points,
                'is_mentor': user.is_mentor,
                'is_premium': user.is_premium,
                'joined_date': user.created_at.isoformat(),
                'last_active': cache.get(f'user_last_activity:{user.id}'),
            },
            'achievements': {
                'total_achievements': UserAchievement.objects.filter(user=user).count(),
                'recent_achievements': list(
                    UserAchievement.objects.filter(
                        user=user,
                        earned_at__gte=thirty_days_ago
                    ).values('achievement__name', 'earned_at')
                ),
            },
            'skills': {
                'total_skills': UserSkill.objects.filter(user=user).count(),
                'expert_skills': UserSkill.objects.filter(
                    user=user,
                    proficiency_level='expert'
                ).count(),
                'endorsed_skills': UserSkill.objects.filter(
                    user=user,
                    endorsements_count__gt=0
                ).count(),
            },
            'learning': {
                'enrolled_courses': UserCourseProgress.objects.filter(user=user).count(),
                'completed_courses': UserCourseProgress.objects.filter(
                    user=user,
                    status='completed'
                ).count(),
                'in_progress_courses': UserCourseProgress.objects.filter(
                    user=user,
                    status='in_progress'
                ).count(),
            },
            'community': {
                'total_posts': CommunityPost.objects.filter(author=user).count(),
                'total_likes': CommunityPost.objects.filter(author=user).aggregate(
                    total=Sum('likes_count')
                )['total'] or 0,
                'recent_posts': CommunityPost.objects.filter(
                    author=user,
                    created_at__gte=thirty_days_ago
                ).count(),
            },
            'jobs': {
                'job_applications': JobApplication.objects.filter(user=user).count(),
                'pending_applications': JobApplication.objects.filter(
                    user=user,
                    status='applied'
                ).count(),
            },
            'mentoring': {
                'is_mentor': user.is_mentor,
                'mentoring_sessions': MentorSession.objects.filter(mentor=user).count() if user.is_mentor else 0,
                'completed_sessions': MentorSession.objects.filter(
                    mentor=user,
                    status='completed'
                ).count() if user.is_mentor else 0,
            }
        }

    @staticmethod
    def get_platform_stats():
        """
        Get overall platform statistics.
        
        Returns:
            Dictionary of platform statistics
        """
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        
        return {
            'users': {
                'total_users': User.objects.count(),
                'active_users': User.objects.filter(
                    last_login__gte=thirty_days_ago
                ).count(),
                'mentors': User.objects.filter(is_mentor=True).count(),
                'premium_users': User.objects.filter(is_premium=True).count(),
            },
            'content': {
                'total_posts': CommunityPost.objects.count(),
                'posts_this_month': CommunityPost.objects.filter(
                    created_at__gte=thirty_days_ago
                ).count(),
                'total_resumes': Resume.objects.count(),
                'total_courses': UserCourseProgress.objects.count(),
            },
            'engagement': {
                'average_user_points': User.objects.aggregate(Avg('points'))['points__avg'] or 0,
                'total_achievements_earned': UserAchievement.objects.count(),
                'skills_endorsed': UserSkill.objects.filter(endorsements_count__gt=0).count(),
            },
            'jobs': {
                'total_applications': JobApplication.objects.count(),
                'applications_this_month': JobApplication.objects.filter(
                    created_at__gte=thirty_days_ago
                ).count(),
            }
        }

    @staticmethod
    def get_activity_heatmap(days=30):
        """
        Get user activity heatmap for the last N days.
        
        Args:
            days: Number of days to include
        
        Returns:
            Dictionary with daily activity counts
        """
        heatmap = {}
        
        for i in range(days):
            date = timezone.now().date() - timedelta(days=i)
            day_start = timezone.make_aware(datetime.combine(date, datetime.min.time()))
            day_end = timezone.make_aware(datetime.combine(date, datetime.max.time()))
            
            activity_count = CommunityPost.objects.filter(
                created_at__range=[day_start, day_end]
            ).count()
            
            heatmap[date.isoformat()] = activity_count
        
        return heatmap

    @staticmethod
    def get_skill_analytics():
        """
        Get analytics on skill endorsements and popularity.
        
        Returns:
            Dictionary of skill analytics
        """
        return {
            'most_endorsed_skills': list(
                UserSkill.objects.values('skill__name', 'skill__category') \
                    .annotate(total_endorsements=Sum('endorsements_count')) \
                    .order_by('-total_endorsements')[:20]
            ),
            'most_common_skills': list(
                UserSkill.objects.values('skill__name', 'skill__category') \
                    .annotate(user_count=Count('user')) \
                    .order_by('-user_count')[:20]
            ),
            'expert_count_by_skill': list(
                UserSkill.objects.filter(proficiency_level='expert') \
                    .values('skill__name', 'skill__category') \
                    .annotate(expert_count=Count('user')) \
                    .order_by('-expert_count')[:20]
            ),
        }

    @staticmethod
    def get_course_analytics():
        """
        Get analytics on course enrollment and completion.
        
        Returns:
            Dictionary of course analytics
        """
        return {
            'most_enrolled_courses': list(
                UserCourseProgress.objects.values('course__title', 'course__id') \
                    .annotate(enrollment_count=Count('user')) \
                    .order_by('-enrollment_count')[:10]
            ),
            'completion_rate': {
                'total_enrollments': UserCourseProgress.objects.count(),
                'total_completions': UserCourseProgress.objects.filter(
                    status='completed'
                ).count(),
                'completion_percentage': (
                    (UserCourseProgress.objects.filter(status='completed').count() /
                     UserCourseProgress.objects.count() * 100)
                    if UserCourseProgress.objects.count() > 0 else 0
                )
            },
            'average_course_rating': UserCourseProgress.objects.aggregate(
                avg_rating=Avg('course__rating')
            )['avg_rating'] or 0,
        }

    @staticmethod
    def get_job_analytics():
        """
        Get analytics on job applications and matches.
        
        Returns:
            Dictionary of job analytics
        """
        return {
            'total_applications': JobApplication.objects.count(),
            'application_status': {
                'applied': JobApplication.objects.filter(status='applied').count(),
                'interview': JobApplication.objects.filter(status='interview').count(),
                'rejected': JobApplication.objects.filter(status='rejected').count(),
                'accepted': JobApplication.objects.filter(status='accepted').count(),
            },
            'applications_by_job_type': dict(
                JobApplication.objects.values('job__job_type') \
                    .annotate(count=Count('id')) \
                    .values_list('job__job_type', 'count')
            ),
            'top_applied_locations': list(
                JobApplication.objects.values('job__location') \
                    .annotate(count=Count('id')) \
                    .order_by('-count')[:10]
            ),
        }

    @staticmethod
    def get_user_growth():
        """
        Get user growth analytics.
        
        Returns:
            Dictionary with user growth data
        """
        now = timezone.now()
        growth = {}
        
        for months_back in range(12):
            month_start = now.replace(day=1) - timedelta(days=30 * months_back)
            month_end = month_start + timedelta(days=30)
            
            month_key = month_start.strftime('%Y-%m')
            growth[month_key] = User.objects.filter(
                created_at__range=[month_start, month_end]
            ).count()
        
        return growth

    @staticmethod
    def get_mentoring_analytics():
        """
        Get analytics on mentoring sessions and ratings.
        
        Returns:
            Dictionary of mentoring analytics
        """
        completed_sessions = MentorSession.objects.filter(status='completed')
        
        return {
            'total_sessions': MentorSession.objects.count(),
            'completed_sessions': completed_sessions.count(),
            'pending_sessions': MentorSession.objects.filter(status='pending').count(),
            'average_rating': completed_sessions.aggregate(
                avg_rating=Avg('rating')
            )['avg_rating'] or 0,
            'top_mentors': list(
                User.objects.filter(mentor__isnull=False) \
                    .annotate(session_count=Count('mentor__mentees')) \
                    .order_by('-session_count')[:10] \
                    .values('id', 'username', 'session_count')
            ),
        }

    @staticmethod
    def generate_engagement_report(user_id=None):
        """
        Generate engagement report for user or platform.
        
        Args:
            user_id: Optional user ID for individual report
        
        Returns:
            Engagement report dictionary
        """
        if user_id:
            user = User.objects.get(id=user_id)
            return AnalyticsService.get_user_stats(user)
        else:
            return {
                'platform': AnalyticsService.get_platform_stats(),
                'skills': AnalyticsService.get_skill_analytics(),
                'courses': AnalyticsService.get_course_analytics(),
                'jobs': AnalyticsService.get_job_analytics(),
                'mentoring': AnalyticsService.get_mentoring_analytics(),
                'growth': AnalyticsService.get_user_growth(),
            }

    @staticmethod
    def cache_analytics():
        """
        Cache expensive analytics computations.
        """
        cache.set('platform_stats', AnalyticsService.get_platform_stats(), timeout=3600)
        cache.set('skill_analytics', AnalyticsService.get_skill_analytics(), timeout=3600)
        cache.set('course_analytics', AnalyticsService.get_course_analytics(), timeout=3600)
        cache.set('job_analytics', AnalyticsService.get_job_analytics(), timeout=3600)
        logger.info("Analytics cached for 1 hour")
