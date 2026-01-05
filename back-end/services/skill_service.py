"""
Skill management service.
Handles skill operations, endorsements, proficiency management, and skill recommendations.
"""

import logging
from django.db.models import Q, Count, Avg, F
from django.db import transaction
from api.models import Skill, UserSkill, Resume
from collections import Counter

logger = logging.getLogger(__name__)


class SkillService:
    """Service for skill management and recommendations."""

    @staticmethod
    def add_skill_to_user(user, skill_id, proficiency_level='beginner', years_of_experience=0):
        """
        Add a skill to user's profile.
        
        Args:
            user: User object
            skill_id: Skill ID
            proficiency_level: beginner, intermediate, advanced, expert
            years_of_experience: Years of experience with skill
        
        Returns:
            UserSkill object
        """
        skill = Skill.objects.get(id=skill_id)
        
        user_skill, created = UserSkill.objects.get_or_create(
            user=user,
            skill=skill,
            defaults={
                'proficiency_level': proficiency_level,
                'years_of_experience': years_of_experience
            }
        )
        
        if not created:
            user_skill.proficiency_level = proficiency_level
            user_skill.years_of_experience = years_of_experience
            user_skill.save()
        
        logger.info(f"Skill {skill.name} added to user {user.id}")
        return user_skill

    @staticmethod
    def remove_skill_from_user(user, skill_id):
        """
        Remove a skill from user's profile.
        
        Args:
            user: User object
            skill_id: Skill ID
        """
        UserSkill.objects.filter(user=user, skill_id=skill_id).delete()
        logger.info(f"Skill {skill_id} removed from user {user.id}")

    @staticmethod
    def endorse_skill(endorser, user, skill_id):
        """
        Endorse another user's skill.
        
        Args:
            endorser: User doing the endorsing
            user: User being endorsed
            skill_id: Skill being endorsed
        
        Returns:
            Updated UserSkill object
        """
        user_skill = UserSkill.objects.get(user=user, skill_id=skill_id)
        user_skill.endorsements_count += 1
        user_skill.save()
        
        # Award points to endorsed user
        user.points += 5
        user.save()
        
        logger.info(f"User {endorser.id} endorsed skill {skill_id} of user {user.id}")
        return user_skill

    @staticmethod
    def get_skill_gaps(user):
        """
        Get recommended skills to learn based on job market and user's profile.
        
        Args:
            user: User object
        
        Returns:
            List of recommended skills with reasoning
        """
        # Get user's current skills
        user_skills = set(UserSkill.objects.filter(user=user).values_list('skill_id', flat=True))
        
        # Get all skills from active job postings
        from api.models import JobOpportunity
        job_skills = set(
            Skill.objects.filter(
                jobtags__job__status='active'
            ).values_list('id', flat=True)
        )
        
        # Get skills from completed resumes
        resume_skills = set(
            Skill.objects.filter(
                userskill__user__resume__isnull=False
            ).values_list('id', flat=True)
        )
        
        # Find gap skills (not in user's profile but in-demand)
        gap_skills = (job_skills | resume_skills) - user_skills
        
        # Rank by frequency
        recommended = []
        for skill_id in gap_skills:
            skill = Skill.objects.get(id=skill_id)
            
            # Count occurrences in jobs
            job_count = JobOpportunity.objects.filter(
                jobtags__skill_id=skill_id,
                status='active'
            ).count()
            
            recommended.append({
                'skill_id': skill.id,
                'skill_name': skill.name,
                'skill_category': skill.category,
                'job_count': job_count,
                'reason': f'Required in {job_count} active job postings'
            })
        
        # Sort by job count
        recommended.sort(key=lambda x: x['job_count'], reverse=True)
        return recommended[:10]  # Top 10 recommendations

    @staticmethod
    def get_trending_skills():
        """
        Get trending skills across the platform.
        
        Returns:
            List of top trending skills
        """
        trending = UserSkill.objects.values('skill__id', 'skill__name', 'skill__category') \
            .annotate(user_count=Count('user'), avg_endorsements=Avg('endorsements_count')) \
            .order_by('-user_count')[:20]
        
        return list(trending)

    @staticmethod
    def get_skill_demand():
        """
        Get in-demand skills based on job postings.
        
        Returns:
            List of in-demand skills with job counts
        """
        from api.models import JobOpportunity
        
        demand = Skill.objects.filter(
            jobtags__job__status='active'
        ).annotate(
            job_count=Count('jobtags__job', distinct=True)
        ).order_by('-job_count')[:20]
        
        return [{
            'id': skill.id,
            'name': skill.name,
            'category': skill.category,
            'job_demand': skill.job_count
        } for skill in demand]

    @staticmethod
    def get_skill_statistics(skill_id):
        """
        Get statistics for a specific skill.
        
        Args:
            skill_id: Skill ID
        
        Returns:
            Skill statistics
        """
        skill = Skill.objects.get(id=skill_id)
        
        user_skills = UserSkill.objects.filter(skill=skill)
        
        return {
            'skill_id': skill.id,
            'skill_name': skill.name,
            'skill_category': skill.category,
            'total_users': user_skills.count(),
            'avg_endorsements': user_skills.aggregate(Avg('endorsements_count'))['endorsements_count__avg'] or 0,
            'proficiency_distribution': {
                'beginner': user_skills.filter(proficiency_level='beginner').count(),
                'intermediate': user_skills.filter(proficiency_level='intermediate').count(),
                'advanced': user_skills.filter(proficiency_level='advanced').count(),
                'expert': user_skills.filter(proficiency_level='expert').count(),
            }
        }

    @staticmethod
    def batch_add_skills(user, skills_data):
        """
        Add multiple skills to user in one transaction.
        
        Args:
            user: User object
            skills_data: List of {skill_id, proficiency_level, years_of_experience}
        
        Returns:
            List of created UserSkill objects
        """
        with transaction.atomic():
            created_skills = []
            for skill_data in skills_data:
                user_skill = SkillService.add_skill_to_user(
                    user,
                    skill_data['skill_id'],
                    skill_data.get('proficiency_level', 'beginner'),
                    skill_data.get('years_of_experience', 0)
                )
                created_skills.append(user_skill)
            return created_skills
