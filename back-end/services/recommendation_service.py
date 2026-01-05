"""
Recommendation engine service.
Generates job, course, mentor, and skill recommendations for users.
"""

import logging
from django.db.models import Q, Count, Avg, F
from api.models import (
    JobOpportunity, Course, Mentor, Skill, UserSkill,
    User, UserCourseProgress, JobApplication
)
from collections import defaultdict
import math

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service for generating personalized recommendations."""

    @staticmethod
    def recommend_jobs(user, limit=10):
        """
        Recommend jobs based on user's skills and preferences.
        
        Args:
            user: User object
            limit: Number of recommendations
        
        Returns:
            List of recommended jobs
        """
        # Get user's skills
        user_skills = set(UserSkill.objects.filter(user=user).values_list('skill_id', flat=True))
        
        if not user_skills:
            # If no skills, recommend trending jobs
            return JobOpportunity.objects.filter(
                status='active'
            ).order_by('-posted_at')[:limit].values(
                'id', 'title', 'company_name', 'location', 'job_type', 'salary_min', 'salary_max'
            )
        
        # Get jobs matching user's skills
        matching_jobs = JobOpportunity.objects.filter(
            status='active'
        ).annotate(
            matching_skills=Count(
                'required_skills',
                filter=Q(required_skills__in=user_skills)
            )
        ).order_by('-matching_skills', '-posted_at')[:limit]
        
        recommendations = []
        for job in matching_jobs:
            skill_match_percentage = (job.matching_skills / job.required_skills.count()) * 100 if job.required_skills.count() > 0 else 0
            
            recommendations.append({
                'job_id': job.id,
                'title': job.title,
                'company_name': job.company_name,
                'location': job.location,
                'job_type': job.job_type,
                'salary_min': job.salary_min,
                'salary_max': job.salary_max,
                'skill_match_percentage': min(100, int(skill_match_percentage)),
                'reason': f'{int(skill_match_percentage)}% of your skills match'
            })
        
        return recommendations

    @staticmethod
    def recommend_courses(user, limit=10):
        """
        Recommend courses based on skill gaps and interests.
        
        Args:
            user: User object
            limit: Number of recommendations
        
        Returns:
            List of recommended courses
        """
        from services.skill_service import SkillService
        
        # Get skill gaps
        skill_gaps = SkillService.get_skill_gaps(user)
        gap_skill_ids = [gap['skill_id'] for gap in skill_gaps[:5]]
        
        if not gap_skill_ids:
            # Recommend trending courses
            return Course.objects.all().order_by('-rating')[:limit].values(
                'id', 'title', 'difficulty', 'duration_hours', 'rating'
            )
        
        # Find courses related to gap skills
        recommended_courses = Course.objects.filter(
            required_skills__in=gap_skill_ids
        ).annotate(
            matching_skills=Count('required_skills', filter=Q(required_skills__in=gap_skill_ids)),
            avg_rating=Avg('rating')
        ).order_by('-matching_skills', '-avg_rating')[:limit]
        
        recommendations = []
        for course in recommended_courses:
            gap_skill_coverage = sum(
                1 for gap in skill_gaps if gap['skill_id'] in course.required_skills.values_list('id', flat=True)
            )
            
            recommendations.append({
                'course_id': course.id,
                'title': course.title,
                'difficulty': course.difficulty,
                'duration_hours': course.duration_hours,
                'rating': course.rating,
                'skill_coverage': gap_skill_coverage,
                'reason': f'Learn {gap_skill_coverage} of your target skills'
            })
        
        return recommendations

    @staticmethod
    def recommend_mentors(user, limit=5):
        """
        Recommend mentors based on user's skill gaps and career goals.
        
        Args:
            user: User object
            limit: Number of recommendations
        
        Returns:
            List of recommended mentors
        """
        from services.skill_service import SkillService
        
        # Get skill gaps
        skill_gaps = SkillService.get_skill_gaps(user)
        gap_skill_ids = [gap['skill_id'] for gap in skill_gaps[:5]]
        
        if not gap_skill_ids:
            # Recommend top-rated mentors
            return Mentor.objects.all().order_by('-rating')[:limit].values(
                'id', 'user__id', 'user__username', 'user__first_name',
                'user__last_name', 'specializations', 'hourly_rate', 'rating'
            )
        
        # Find mentors who specialize in gap skills
        recommended_mentors = Mentor.objects.filter(
            user__userskill__skill_id__in=gap_skill_ids
        ).annotate(
            matching_skills=Count(
                'user__userskill__skill',
                filter=Q(user__userskill__skill_id__in=gap_skill_ids),
                distinct=True
            ),
            mentor_rating=Avg('rating')
        ).order_by('-mentor_rating', '-matching_skills')[:limit]
        
        recommendations = []
        for mentor in recommended_mentors:
            recommendations.append({
                'mentor_id': mentor.id,
                'user_id': mentor.user.id,
                'name': mentor.user.get_full_name(),
                'username': mentor.user.username,
                'specializations': mentor.specializations,
                'hourly_rate': mentor.hourly_rate,
                'rating': mentor.rating,
                'matching_skills': mentor.matching_skills,
                'reason': f'Expert in {mentor.matching_skills} of your target skills'
            })
        
        return recommendations

    @staticmethod
    def recommend_skills(user, limit=5):
        """
        Recommend skills based on job market demand and career path.
        
        Args:
            user: User object
            limit: Number of recommendations
        
        Returns:
            List of recommended skills
        """
        from services.skill_service import SkillService
        
        # Get trending and in-demand skills
        trending = SkillService.get_trending_skills()
        in_demand = SkillService.get_skill_demand()
        
        # Combine and rank by demand
        skill_scores = defaultdict(float)
        
        for skill in trending[:10]:
            skill_scores[skill['skill__id']] += skill['user_count']
        
        for skill in in_demand[:10]:
            skill_scores[skill['id']] += skill['job_demand'] * 2  # Weight job demand higher
        
        # Get user's current skills
        user_skills = set(UserSkill.objects.filter(user=user).values_list('skill_id', flat=True))
        
        # Rank recommended skills
        recommendations = []
        for skill_id, score in sorted(skill_scores.items(), key=lambda x: x[1], reverse=True):
            if skill_id not in user_skills:
                try:
                    skill = Skill.objects.get(id=skill_id)
                    recommendations.append({
                        'skill_id': skill.id,
                        'skill_name': skill.name,
                        'category': skill.category,
                        'demand_score': int(score),
                        'reason': 'In high demand across job market'
                    })
                except Skill.DoesNotExist:
                    continue
        
        return recommendations[:limit]

    @staticmethod
    def recommend_connections(user, limit=5):
        """
        Recommend users to connect with based on shared interests and skills.
        
        Args:
            user: User object
            limit: Number of recommendations
        
        Returns:
            List of recommended users
        """
        # Get user's skills
        user_skills = set(UserSkill.objects.filter(user=user).values_list('skill_id', flat=True))
        
        if not user_skills:
            # Recommend active users
            return User.objects.exclude(id=user.id).order_by('-points')[:limit].values(
                'id', 'username', 'first_name', 'last_name', 'title', 'location'
            )
        
        # Find users with similar skills
        similar_users = User.objects.exclude(
            id=user.id
        ).filter(
            userskill__skill_id__in=user_skills
        ).annotate(
            shared_skills=Count('userskill__skill', filter=Q(userskill__skill_id__in=user_skills), distinct=True),
            user_points=F('points')
        ).order_by('-shared_skills', '-user_points')[:limit]
        
        recommendations = []
        for similar_user in similar_users:
            recommendations.append({
                'user_id': similar_user.id,
                'username': similar_user.username,
                'name': similar_user.get_full_name(),
                'title': similar_user.title,
                'location': similar_user.location,
                'shared_skills': similar_user.shared_skills,
                'points': similar_user.user_points,
                'reason': f'Share {similar_user.shared_skills} skills with you'
            })
        
        return recommendations

    @staticmethod
    def get_personalized_dashboard(user):
        """
        Get all recommendations for user's dashboard.
        
        Args:
            user: User object
        
        Returns:
            Dictionary with all recommendations
        """
        return {
            'recommended_jobs': RecommendationService.recommend_jobs(user, limit=5),
            'recommended_courses': RecommendationService.recommend_courses(user, limit=5),
            'recommended_mentors': RecommendationService.recommend_mentors(user, limit=3),
            'recommended_skills': RecommendationService.recommend_skills(user, limit=5),
            'recommended_connections': RecommendationService.recommend_connections(user, limit=5),
        }

    @staticmethod
    def log_recommendation_click(user, recommendation_type, recommendation_id):
        """
        Log when user clicks on a recommendation (for analytics).
        
        Args:
            user: User object
            recommendation_type: Type of recommendation (job, course, mentor, etc.)
            recommendation_id: ID of recommended item
        """
        logger.info(
            f"Recommendation clicked: {recommendation_type} {recommendation_id}",
            extra={
                'user_id': user.id,
                'recommendation_type': recommendation_type,
                'recommendation_id': recommendation_id,
            }
        )
