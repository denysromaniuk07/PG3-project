"""
Recommendation generation tasks.
Generates and caches personalized recommendations for users.
"""

import logging
from celery import shared_task
from api.models import User
from services import RecommendationService
from django.core.cache import cache

logger = logging.getLogger(__name__)


@shared_task
def generate_daily_recommendations():
    """
    Generate recommendations for all active users daily.
    Caches results for faster retrieval.
    """
    try:
        users = User.objects.filter(is_active=True)
        
        for user in users:
            try:
                dashboard = RecommendationService.get_personalized_dashboard(user)
                
                # Cache recommendations for 24 hours
                cache.set(
                    f'user_recommendations:{user.id}',
                    dashboard,
                    timeout=86400  # 24 hours
                )
                
            except Exception as e:
                logger.warning(f"Error generating recommendations for user {user.id}: {str(e)}")
                continue
        
        logger.info(f"Generated recommendations for {users.count()} users")
    
    except Exception as exc:
        logger.error(f"Error in daily recommendations task: {str(exc)}")


@shared_task
def recommend_jobs_async(user_id, limit=10):
    """
    Generate and cache job recommendations for a user.
    
    Args:
        user_id: User ID
        limit: Number of recommendations
    """
    try:
        user = User.objects.get(id=user_id)
        
        jobs = RecommendationService.recommend_jobs(user, limit=limit)
        
        # Cache recommendations
        cache.set(
            f'user_job_recommendations:{user_id}',
            jobs,
            timeout=3600  # 1 hour
        )
        
        logger.info(f"Generated {len(jobs)} job recommendations for user {user_id}")
    
    except Exception as exc:
        logger.error(f"Error recommending jobs for user {user_id}: {str(exc)}")


@shared_task
def recommend_courses_async(user_id, limit=10):
    """
    Generate and cache course recommendations for a user.
    
    Args:
        user_id: User ID
        limit: Number of recommendations
    """
    try:
        user = User.objects.get(id=user_id)
        
        courses = RecommendationService.recommend_courses(user, limit=limit)
        
        # Cache recommendations
        cache.set(
            f'user_course_recommendations:{user_id}',
            courses,
            timeout=3600  # 1 hour
        )
        
        logger.info(f"Generated {len(courses)} course recommendations for user {user_id}")
    
    except Exception as exc:
        logger.error(f"Error recommending courses for user {user_id}: {str(exc)}")


@shared_task
def recommend_mentors_async(user_id, limit=5):
    """
    Generate and cache mentor recommendations for a user.
    
    Args:
        user_id: User ID
        limit: Number of recommendations
    """
    try:
        user = User.objects.get(id=user_id)
        
        mentors = RecommendationService.recommend_mentors(user, limit=limit)
        
        # Cache recommendations
        cache.set(
            f'user_mentor_recommendations:{user_id}',
            mentors,
            timeout=3600  # 1 hour
        )
        
        logger.info(f"Generated {len(mentors)} mentor recommendations for user {user_id}")
    
    except Exception as exc:
        logger.error(f"Error recommending mentors for user {user_id}: {str(exc)}")


@shared_task
def recommend_skills_async(user_id, limit=5):
    """
    Generate and cache skill recommendations for a user.
    
    Args:
        user_id: User ID
        limit: Number of recommendations
    """
    try:
        user = User.objects.get(id=user_id)
        
        skills = RecommendationService.recommend_skills(user, limit=limit)
        
        # Cache recommendations
        cache.set(
            f'user_skill_recommendations:{user_id}',
            skills,
            timeout=3600  # 1 hour
        )
        
        logger.info(f"Generated {len(skills)} skill recommendations for user {user_id}")
    
    except Exception as exc:
        logger.error(f"Error recommending skills for user {user_id}: {str(exc)}")


@shared_task
def recommend_connections_async(user_id, limit=5):
    """
    Generate and cache connection recommendations for a user.
    
    Args:
        user_id: User ID
        limit: Number of recommendations
    """
    try:
        user = User.objects.get(id=user_id)
        
        connections = RecommendationService.recommend_connections(user, limit=limit)
        
        # Cache recommendations
        cache.set(
            f'user_connection_recommendations:{user_id}',
            connections,
            timeout=3600  # 1 hour
        )
        
        logger.info(f"Generated {len(connections)} connection recommendations for user {user_id}")
    
    except Exception as exc:
        logger.error(f"Error recommending connections for user {user_id}: {str(exc)}")


@shared_task
def batch_recommend_jobs():
    """
    Generate job recommendations for all users.
    """
    try:
        users = User.objects.filter(is_active=True)
        
        for user in users:
            recommend_jobs_async.delay(user.id, limit=10)
        
        logger.info(f"Queued job recommendations for {users.count()} users")
    
    except Exception as exc:
        logger.error(f"Error in batch job recommendations: {str(exc)}")
