"""
Business logic services for the backend.

This package contains service classes that handle business logic,
data transformations, and complex operations.

Services included:
- ResumeService: Resume processing and ML analysis
- SkillService: Skill management and recommendations
- AchievementService: Achievement unlocking and tracking
- NotificationService: User notifications and alerts
- RecommendationService: Personalized recommendations
- AnalyticsService: Activity tracking and reporting
"""

from .resume_service import ResumeService
from .skill_service import SkillService
from .achievement_service import AchievementService
from .notification_service import NotificationService
from .recommendation_service import RecommendationService
from .analytics_service import AnalyticsService

__all__ = [
    'ResumeService',
    'SkillService',
    'AchievementService',
    'NotificationService',
    'RecommendationService',
    'AnalyticsService',
]
